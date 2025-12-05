"""Flask application."""

from flask import Flask, render_template, request, redirect
from urllib.parse import quote_plus
import requests

from models.db import init_db
from services.edgar import search_firms, get_filings_for_cik
from services.rss import search_releases
from services.metrics import calculate_metrics
from services.s1_mining import get_portfolio_exits
from services.form_adv import get_adv_for_firm
from data.vc_firms import search_curated_vcs, get_curated_vc_by_cik
from config import EDGAR_USER_AGENT

app = Flask(__name__)

with app.app_context():
    init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    """HTMX endpoint - two-tier search: curated first, EDGAR on demand."""
    query = request.args.get("q", "").strip()
    edgar_only = request.args.get("edgar", "0") == "1"
    
    if len(query) < 2:
        return render_template("partials/firm_dropdown.html", 
                             curated_results=[], edgar_results=[], 
                             query=query, show_edgar_option=False)
    
    if edgar_only:
        edgar_results = search_firms(query, max_results=10)
        return render_template("partials/firm_dropdown.html",
                             curated_results=[], edgar_results=edgar_results,
                             query=query, show_edgar_option=False)
    
    curated_results = search_curated_vcs(query, limit=8)
    return render_template("partials/firm_dropdown.html",
                         curated_results=curated_results, edgar_results=[],
                         query=query, show_edgar_option=True)


@app.route("/search-firm")
def search_firm_redirect():
    """Search EDGAR for a firm by name - always shows EDGAR results."""
    name = request.args.get("name", "").strip()
    website = request.args.get("website", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 10
    
    if not name:
        return "No firm name provided", 400
    
    # Search EDGAR - get extra results for pagination
    all_results = search_firms(name, max_results=per_page * (page + 1))
    
    # Prioritize curated VCs at top of first page
    if page == 1:
        curated_ciks = set()
        for vc in search_curated_vcs(name, limit=5):
            if vc.get("cik"):
                curated_ciks.add(vc["cik"])
        
        # Move curated matches to front
        curated_results = [r for r in all_results if r.cik in curated_ciks]
        other_results = [r for r in all_results if r.cik not in curated_ciks]
        all_results = curated_results + other_results
    
    # Paginate
    start = (page - 1) * per_page
    end = start + per_page
    results = all_results[start:end]
    
    has_prev = page > 1
    has_next = len(all_results) > end
    
    return render_template("search_results.html", 
                         results=results, 
                         query=name,
                         website=website,
                         page=page,
                         has_prev=has_prev,
                         has_next=has_next)


@app.route("/firm/<cik>")
def firm_profile(cik: str):
    """Display firm profile with metrics."""
    cik = cik.lstrip("0")
    website_param = request.args.get("website", "").strip()
    curated_vc = get_curated_vc_by_cik(cik)
    
    # Use website from URL param if not in curated database
    if website_param and curated_vc and not curated_vc.get("website"):
        curated_vc = dict(curated_vc)  # Make a copy
        curated_vc["website"] = website_param
    
    # Store website separately for non-curated VCs
    external_website = website_param if not curated_vc else None
    
    # Get firm name from SEC
    try:
        padded_cik = cik.zfill(10)
        headers = {"User-Agent": EDGAR_USER_AGENT}
        resp = requests.get(f"https://data.sec.gov/submissions/CIK{padded_cik}.json",
                          headers=headers, timeout=30)
        firm_name = resp.json().get("name", "Unknown")
    except:
        firm_name = curated_vc["name"] if curated_vc else "Unknown"
    
    filings = get_filings_for_cik(cik)
    
    if not filings and not curated_vc:
        return f"No Form D filings found for CIK {cik}", 404
    
    # Use the SEC entity name from filings (most accurate for searches)
    sec_entity_name = filings[0].issuer_name if filings else firm_name
    display_name = curated_vc.get("name", firm_name) if curated_vc else firm_name
    
    firm = {
        "cik": cik,
        "name": display_name,
        "sec_entity_name": sec_entity_name,  # Exact legal name from SEC
        "curated": curated_vc,
        "website": (curated_vc.get("website") if curated_vc else None) or external_website,
    }
    
    # Collect related persons
    people_seen = set()
    people = []
    for f in filings:
        for p in f.related_persons:
            if p["name"] not in people_seen:
                people_seen.add(p["name"])
                people.append(p)
    
    metrics = calculate_metrics(filings)
    
    # Fetch Form ADV data (AUM, disclosures, etc.)
    form_adv = None
    try:
        form_adv = get_adv_for_firm(display_name)
    except Exception as e:
        print(f"Form ADV fetch error: {e}")
    
    # OSINT links - cleaned up, only useful ones
    sec_name_encoded = quote_plus(sec_entity_name)
    display_name_encoded = quote_plus(display_name)
    
    osint_links = {
        "SEC EDGAR (All Filings)": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40",
        "Google News": f"https://www.google.com/search?q={display_name_encoded}+funding+OR+investment&tbm=nws",
        "Crunchbase": f"https://www.crunchbase.com/textsearch?q={display_name_encoded}",
        "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={display_name_encoded}",
    }
    
    if curated_vc and curated_vc.get("website"):
        osint_links = {"Official Website": curated_vc["website"], **osint_links}
    
    # Add Form ADV link if we found data
    if form_adv and form_adv.crd_number:
        osint_links["SEC Form ADV Details"] = f"https://adviserinfo.sec.gov/firm/summary/{form_adv.crd_number}"
    
    try:
        press_releases = search_releases(firm["name"])[:5]
    except:
        press_releases = []
    
    return render_template(
        "profile.html",
        firm=firm,
        filings=filings[:20],
        people=people[:15],
        metrics=metrics,
        osint_links=osint_links,
        press_releases=press_releases,
        form_adv=form_adv,
    )


@app.route("/portfolio-exits/<name>")
def portfolio_exits(name: str):
    """Fetch S-1 filings and extract ownership data (HTMX endpoint)."""
    exits = get_portfolio_exits(name, limit=8)
    return render_template("partials/portfolio_exits.html", exits=exits, vc_name=name)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

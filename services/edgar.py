"""SEC EDGAR API client."""

import time
import requests
from lxml import etree
from dataclasses import dataclass
from datetime import date
from typing import Optional
from config import EDGAR_SEARCH_URL, EDGAR_FILING_URL, EDGAR_USER_AGENT, EDGAR_RATE_LIMIT


# Rate limiting
_last_request_time = 0.0


def _rate_limit():
    """Enforce SEC's 10 requests/second limit."""
    global _last_request_time
    min_interval = 1.0 / EDGAR_RATE_LIMIT
    elapsed = time.time() - _last_request_time
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)
    _last_request_time = time.time()


def _get(url: str, params: dict = None) -> requests.Response:
    """Make a rate-limited GET request."""
    _rate_limit()
    headers = {"User-Agent": EDGAR_USER_AGENT}
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp


@dataclass
class FirmSearchResult:
    cik: str
    name: str
    recent_filing: str
    filing_count: int


def _get_company_info(cik: str) -> dict:
    """Fetch company info from SEC submissions API."""
    padded_cik = cik.lstrip("0").zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
    
    try:
        resp = _get(url)
        data = resp.json()
        
        # Count Form D filings
        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        filing_dates = recent.get("filingDate", [])
        
        form_d_count = 0
        latest_date = ""
        for i, form in enumerate(forms):
            if form in ("D", "D/A"):
                form_d_count += 1
                if i < len(filing_dates) and filing_dates[i] > latest_date:
                    latest_date = filing_dates[i]
        
        return {
            "name": data.get("name", "Unknown"),
            "cik": cik.lstrip("0"),
            "filing_count": form_d_count,
            "recent_filing": latest_date,
        }
    except:
        return None


def _generate_name_variations(query: str) -> list[str]:
    """
    Generate search variations:
    - Original query
    - Swap 'Capital' <-> 'Ventures'
    - Just the first word
    """
    variations = [query]
    query_lower = query.lower()
    
    # Capital <-> Ventures swap
    if "capital" in query_lower:
        variations.append(query_lower.replace("capital", "ventures").title())
    elif "ventures" in query_lower:
        variations.append(query_lower.replace("ventures", "capital").title())
    
    # Just first word (if multi-word)
    words = query.split()
    if len(words) > 1:
        variations.append(words[0])
    
    return variations


def search_firms(query: str, max_results: int = 10) -> list[FirmSearchResult]:
    """
    Search for firms by name using multiple approaches:
    1. SEC company name search API with name variations
    2. SEC full-text search in Form D filings
    Filters: Only results from 2016 onward, sorted by date (most recent first)
    """
    import re
    from urllib.parse import quote_plus
    
    MIN_YEAR = 2016
    seen_ciks = set()
    
    # Generate name variations to search
    search_variations = _generate_name_variations(query)
    
    # Method 1: Try SEC company search API with all variations
    for search_term in search_variations:
        try:
            company_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={quote_plus(search_term)}&type=D&output=atom"
            resp = _get(company_url)
            
            # Parse the atom feed to extract CIKs
            cik_pattern = r'<cik>(\d+)</cik>'
            matches = re.findall(cik_pattern, resp.text)
            for cik in matches[:50]:
                seen_ciks.add(cik.lstrip("0"))
        except Exception as e:
            print(f"Company search error for '{search_term}': {e}")
    
    # Method 2: Also try full-text search with original query
    params = {
        "q": f'"{query}"',
        "forms": "D",
        "dateRange": "custom", 
        "startdt": f"{MIN_YEAR}-01-01",
        "enddt": date.today().isoformat(),
    }
    
    try:
        resp = _get(EDGAR_SEARCH_URL, params)
        data = resp.json()
        
        for hit in data.get("hits", {}).get("hits", []):
            source = hit.get("_source", {})
            ciks = source.get("ciks", [])
            for cik in ciks:
                clean_cik = cik.lstrip("0")
                if clean_cik:
                    seen_ciks.add(clean_cik)
    except Exception as e:
        print(f"Full-text search error: {e}")
    
    # Fetch company info for each CIK - filter to only show VC funds from 2016+
    results = []
    seen_names = set()  # Deduplicate by normalized name
    query_words = [w.lower() for w in query.split()]
    
    for cik in list(seen_ciks)[:max_results * 5]:  # Get more, then filter
        info = _get_company_info(cik)
        if not info or info["filing_count"] == 0:
            continue
        
        # FILTER: No results before 2016
        recent_date = info.get("recent_filing", "")
        if recent_date and recent_date < f"{MIN_YEAR}-01-01":
            continue
        
        name_lower = info["name"].lower()
        
        # Deduplicate by exact name (case-insensitive) - suffixes matter for legal entities
        if name_lower in seen_names:
            continue
        
        # Must match query (contains any query word)
        matches_query = any(w in name_lower for w in query_words)
        if not matches_query:
            continue
        
        # Filter: Only include entities that look like VC funds
        is_likely_fund = any(term in name_lower for term in [
            "venture", "capital", "partners", "fund", "l.p.", "lp", 
            "management", "investors", "holdings", "equity"
        ])
        
        if is_likely_fund:
            seen_names.add(name_lower)
            results.append(FirmSearchResult(
                cik=info["cik"],
                name=info["name"],
                recent_filing=info["recent_filing"],
                filing_count=info["filing_count"],
            ))
        
        if len(results) >= max_results:
            break
    
    # Sort by date, most recent first
    results.sort(key=lambda x: x.recent_filing or "", reverse=True)
    return results


@dataclass
class FormDFiling:
    accession_number: str
    cik: str
    issuer_name: str
    filing_date: date
    is_amendment: bool
    total_offering_amount: Optional[int]
    total_amount_sold: Optional[int]
    total_remaining: Optional[int]
    investor_count: Optional[int]
    minimum_investment: Optional[int]
    industry_group: Optional[str]
    issuer_state: Optional[str]
    issuer_city: Optional[str]
    date_of_first_sale: Optional[date]
    related_persons: list[dict]


def _parse_int(text: Optional[str]) -> Optional[int]:
    """Parse integer, return None if empty or invalid."""
    if not text:
        return None
    try:
        return int(float(text))
    except (ValueError, TypeError):
        return None


def _parse_date(text: Optional[str]) -> Optional[date]:
    """Parse date, return None if empty or invalid."""
    if not text:
        return None
    try:
        from dateutil.parser import parse
        return parse(text).date()
    except:
        return None


def fetch_filing(cik: str, accession_number: str) -> Optional[FormDFiling]:
    """
    Fetch and parse a single Form D filing.
    """
    # Clean up accession number (remove dashes for URL)
    clean_accession = accession_number.replace("-", "")
    clean_cik = cik.lstrip("0")
    
    # Raw XML is at primary_doc.xml (NOT xslFormDX01 which renders HTML)
    url = f"{EDGAR_FILING_URL}/{clean_cik}/{clean_accession}/primary_doc.xml"
    
    try:
        resp = _get(url)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        print(f"HTTP error for {url}: {e}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    
    # Parse XML
    try:
        root = etree.fromstring(resp.content)
    except Exception as e:
        print(f"XML parse error for {accession_number}: {e}")
        return None
    
    # Form D XML has no namespace - just plain element names
    def find_text(path: str) -> Optional[str]:
        elem = root.find(path)
        return elem.text.strip() if elem is not None and elem.text else None
    
    # Related persons
    related_persons = []
    for person in root.findall(".//relatedPersonInfo"):
        name_elem = person.find("relatedPersonName")
        if name_elem is not None:
            first = name_elem.findtext("firstName", default="") or ""
            last = name_elem.findtext("lastName", default="") or ""
            
            relationships = []
            rel_list = person.find("relatedPersonRelationshipList")
            if rel_list is not None:
                for rel in rel_list.findall("relationship"):
                    if rel.text:
                        relationships.append(rel.text)
            
            full_name = f"{first} {last}".strip()
            # Skip "N/A" entries (these are often the GP entity)
            if full_name and full_name != "N/A" and not full_name.startswith("N/A "):
                related_persons.append({
                    "name": full_name,
                    "relationships": relationships,
                })
    
    # Get issuer name
    issuer_name = find_text(".//primaryIssuer/entityName")
    
    # Check if amendment
    submission_type = find_text("submissionType") or ""
    is_amendment = "/A" in submission_type
    
    # Get signature date (most reliable filing date)
    filing_date_str = find_text(".//signatureBlock/signature/signatureDate")
    filing_date = _parse_date(filing_date_str) if filing_date_str else date.today()
    
    return FormDFiling(
        accession_number=accession_number,
        cik=clean_cik,
        issuer_name=issuer_name or "Unknown",
        filing_date=filing_date,
        is_amendment=is_amendment,
        total_offering_amount=_parse_int(find_text(".//offeringData/offeringSalesAmounts/totalOfferingAmount")),
        total_amount_sold=_parse_int(find_text(".//offeringData/offeringSalesAmounts/totalAmountSold")),
        total_remaining=_parse_int(find_text(".//offeringData/offeringSalesAmounts/totalRemaining")),
        investor_count=_parse_int(find_text(".//offeringData/investors/totalNumberAlreadyInvested")),
        minimum_investment=_parse_int(find_text(".//offeringData/minimumInvestmentAccepted")),
        industry_group=find_text(".//offeringData/industryGroup/industryGroupType"),
        issuer_state=find_text(".//primaryIssuer/issuerAddress/stateOrCountry"),
        issuer_city=find_text(".//primaryIssuer/issuerAddress/city"),
        date_of_first_sale=_parse_date(find_text(".//offeringData/typeOfFiling/dateOfFirstSale/value")),
        related_persons=related_persons,
    )


def get_filings_for_cik(cik: str) -> list[FormDFiling]:
    """
    Get all Form D filings for a given CIK using the submissions API.
    """
    clean_cik = cik.lstrip("0")
    padded_cik = clean_cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
    
    try:
        resp = _get(url)
        data = resp.json()
    except Exception as e:
        print(f"Error fetching submissions for {cik}: {e}")
        return []
    
    filings = []
    
    # Get recent filings from the main response
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accessions = recent.get("accessionNumber", [])
    
    # Find Form D filings (limit to 20 most recent)
    count = 0
    for i, form in enumerate(forms):
        if form in ("D", "D/A"):
            if count >= 20:
                break
            
            accession = accessions[i] if i < len(accessions) else None
            if not accession:
                continue
            
            filing = fetch_filing(clean_cik, accession)
            if filing:
                filings.append(filing)
                count += 1
    
    filings.sort(key=lambda x: x.filing_date, reverse=True)
    return filings


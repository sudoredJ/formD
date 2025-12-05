"""
S-1 Mining Service - Find portfolio company IPOs mentioning a VC as investor.
"""

import requests
import re
from dataclasses import dataclass
from config import EDGAR_USER_AGENT


@dataclass
class S1Hit:
    """An S-1/IPO filing that mentions a VC."""
    company_name: str
    cik: str
    filing_date: str
    form_type: str
    accession: str
    url: str


def search_s1_mentions(vc_name: str, limit: int = 10) -> list[S1Hit]:
    """
    Search SEC EDGAR for S-1 filings mentioning a VC as an investor.
    Uses EXACT phrase match on the full VC name to avoid false positives.
    """
    base_url = "https://efts.sec.gov/LATEST/search-index"
    headers = {"User-Agent": EDGAR_USER_AGENT}
    
    # Clean the name but keep it specific - remove LP/LLC suffix only
    search_name = re.sub(r',?\s*(L\.?P\.?|LLC|Inc\.?)\.?$', '', vc_name, flags=re.IGNORECASE).strip()
    
    # Must have at least 2 words to be specific enough
    if len(search_name.split()) < 2:
        # For single-word names, append common suffixes to search
        base = search_name
        search_terms = [f'"{base} Capital"', f'"{base} Ventures"', f'"{base} Partners"']
    else:
        search_terms = [f'"{search_name}"']
    
    seen_companies = set()
    results = []
    
    for search_term in search_terms:
        if len(results) >= limit:
            break
            
        params = {
            "q": search_term,
            "forms": "S-1,S-1/A",
            "dateRange": "custom",
            "startdt": "2012-01-01",
            "enddt": "2025-12-31",
        }
        
        try:
            resp = requests.get(base_url, params=params, headers=headers, timeout=15)
            
            if resp.status_code != 200:
                continue
            
            data = resp.json()
            hits = data.get("hits", {}).get("hits", [])
            
            for hit in hits:
                if len(results) >= limit:
                    break
                
                source = hit.get("_source", {})
                
                # Only process main S-1 documents, not exhibits
                file_type = source.get("file_type", "")
                if file_type.startswith("EX-"):
                    continue  # Skip exhibits - they cause false positives
                
                # Get company name
                display_names = source.get("display_names", [])
                if not display_names:
                    continue
                
                company_name = display_names[0].split("(CIK")[0].strip()
                company_key = company_name.lower()
                
                # Skip duplicates
                if company_key in seen_companies:
                    continue
                
                # Skip if company name contains the VC name (it's the VC itself, not a portfolio co)
                vc_words = search_name.lower().split()
                if all(w in company_key for w in vc_words[:2]):
                    continue
                
                # Filter out non-VC portfolio companies
                if not _is_likely_vc_portfolio(company_name):
                    continue
                
                seen_companies.add(company_key)
                
                ciks = source.get("ciks", [])
                cik = ciks[0].lstrip("0") if ciks else ""
                filing_date = source.get("file_date", "")
                form = source.get("form", "S-1")
                accession = source.get("adsh", "")
                
                # Build URL to filing index
                accession_clean = accession.replace("-", "")
                doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_clean}/"
                
                results.append(S1Hit(
                    company_name=company_name,
                    cik=cik,
                    filing_date=filing_date,
                    form_type=form,
                    accession=accession,
                    url=doc_url,
                ))
                
        except Exception as e:
            print(f"S-1 search error: {e}")
            continue
    
    # Sort by date, most recent first
    results.sort(key=lambda x: x.filing_date or "", reverse=True)
    return results


def _is_likely_vc_portfolio(company_name: str) -> bool:
    """Filter out companies that are clearly NOT VC portfolio companies."""
    name_lower = company_name.lower()
    
    exclude_terms = [
        # Real estate
        "realty", "real estate", "reit", "properties", "mortgage", "housing",
        # Finance/banking
        "bancorp", "bancshares", "bank of", "savings bank", "insurance", "assurance",
        # Energy
        "oil", "gas", "petroleum", "mining", "minerals", "coal", "drilling",
        # Industrial
        "steel", "aluminum", "cement", "chemical",
        # Utilities
        "electric", "utility", "power company",
        # Other
        "restaurant", "grocery", "trucking", "casino", "gaming",
        # SPACs (usually noise)
        "acquisition corp", "blank check",
    ]
    
    return not any(term in name_lower for term in exclude_terms)


def get_portfolio_exits(vc_name: str, limit: int = 8) -> list[dict]:
    """Get portfolio company IPOs for a VC."""
    hits = search_s1_mentions(vc_name, limit=limit)
    
    return [
        {
            "company": hit.company_name,
            "ipo_date": hit.filing_date,
            "form_type": hit.form_type,
            "s1_url": hit.url,
        }
        for hit in hits
    ]

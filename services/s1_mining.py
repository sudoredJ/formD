"""
S-1 Mining Service - Extract portfolio company exit data from IPO filings.

S-1 filings contain "Principal Stockholders" sections with:
- Investor entity names
- Share counts
- Ownership percentages
"""

import requests
import re
from dataclasses import dataclass
from typing import Optional
from config import EDGAR_USER_AGENT
import time


@dataclass
class S1Hit:
    """An S-1 filing that mentions a VC."""
    company_name: str
    cik: str
    filing_date: str
    form_type: str
    accession: str
    url: str


@dataclass
class OwnershipEntry:
    """Ownership entry extracted from S-1."""
    investor_name: str
    shares: Optional[int]
    percentage: Optional[float]
    notes: str


def search_s1_mentions(vc_name: str, limit: int = 10) -> list[S1Hit]:
    """
    Search SEC EDGAR for S-1 filings that mention a VC firm.
    Returns list of S-1 filings.
    """
    url = "https://efts.sec.gov/LATEST/search-index"
    
    params = {
        "q": f'"{vc_name}"',
        "forms": "S-1",
        "dateRange": "custom",
        "startdt": "2015-01-01",
        "enddt": "2025-12-31",
    }
    
    headers = {"User-Agent": EDGAR_USER_AGENT}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        if resp.status_code != 200:
            return []
        
        data = resp.json()
        hits = data.get("hits", {}).get("hits", [])
        
        results = []
        seen_companies = set()
        
        for hit in hits:
            source = hit.get("_source", {})
            
            # Only process main S-1 documents (not exhibits)
            file_type = source.get("file_type", "")
            if file_type not in ["S-1", "S-1/A"]:
                continue
            
            # Get company info
            display_names = source.get("display_names", [])
            if not display_names:
                continue
            
            company_name = display_names[0].split("(CIK")[0].strip()
            ciks = source.get("ciks", [])
            cik = ciks[0].lstrip("0") if ciks else ""
            
            # Skip if we've already seen this company
            if company_name in seen_companies:
                continue
            seen_companies.add(company_name)
            
            filing_date = source.get("file_date", "")
            accession = source.get("adsh", "")
            
            # Build URL
            accession_clean = accession.replace("-", "")
            file_id = hit.get("_id", "").split(":")[-1]
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_clean}/{file_id}"
            
            results.append(S1Hit(
                company_name=company_name,
                cik=cik,
                filing_date=filing_date,
                form_type=file_type,
                accession=accession,
                url=doc_url,
            ))
            
            if len(results) >= limit:
                break
        
        return results
    
    except Exception as e:
        print(f"S-1 search error: {e}")
        return []


def extract_ownership_mentions(s1_url: str, vc_name: str) -> list[str]:
    """
    Fetch an S-1 and extract text mentioning the VC.
    Returns relevant snippets.
    """
    headers = {"User-Agent": EDGAR_USER_AGENT}
    
    try:
        time.sleep(0.2)  # Rate limit
        resp = requests.get(s1_url, headers=headers, timeout=30)
        if resp.status_code != 200:
            return []
        
        html = resp.text
        
        # Find mentions of the VC
        vc_pattern = re.escape(vc_name)
        mentions = []
        
        # Look for share counts near VC name
        # Pattern: "X shares of Class A common stock held ... by [VC name]"
        share_pattern = rf'([\d,]+)\s*shares[^<]*{vc_pattern}'
        matches = re.findall(share_pattern, html, re.IGNORECASE)
        
        for match in matches[:5]:
            mentions.append(f"{match} shares")
        
        # Look for percentage mentions
        pct_pattern = rf'{vc_pattern}[^<]*?([\d.]+)%'
        pct_matches = re.findall(pct_pattern, html, re.IGNORECASE)
        
        for match in pct_matches[:3]:
            mentions.append(f"{match}% ownership")
        
        return mentions
    
    except Exception as e:
        print(f"S-1 extraction error: {e}")
        return []


def get_portfolio_exits(vc_name: str, limit: int = 8) -> list[dict]:
    """
    Get portfolio company IPOs for a VC.
    Returns list of companies with basic ownership info.
    """
    hits = search_s1_mentions(vc_name, limit=limit)
    
    results = []
    for hit in hits:
        result = {
            "company": hit.company_name,
            "ipo_date": hit.filing_date,
            "s1_url": hit.url,
            "mentions": [],
        }
        
        # Try to extract ownership mentions (rate limited)
        mentions = extract_ownership_mentions(hit.url, vc_name)
        result["mentions"] = mentions
        
        results.append(result)
        
        # Be nice to SEC servers
        time.sleep(0.3)
    
    return results


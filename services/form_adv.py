"""SEC Form ADV (Investment Adviser) data fetching."""

import requests
from dataclasses import dataclass
from typing import Optional
from config import EDGAR_USER_AGENT


@dataclass
class FormADVInfo:
    """Form ADV data for an investment adviser."""
    firm_name: str
    crd_number: str
    sec_number: str
    aum: Optional[int]  # Assets under management
    aum_date: Optional[str]
    employee_count: Optional[int]
    state: Optional[str]
    registration_status: str
    has_disclosure_events: bool
    brochure_url: Optional[str]


def search_form_adv(firm_name: str) -> list[dict]:
    """
    Search SEC IAPD for investment adviser by name.
    Returns basic info from search results.
    """
    # SEC IAPD has a public API
    url = "https://api.adviserinfo.sec.gov/IAPD/Content/Search/api/PublicSearch/Search"
    
    headers = {
        "User-Agent": EDGAR_USER_AGENT,
        "Content-Type": "application/json",
    }
    
    payload = {
        "firmName": firm_name,
        "pageNumber": 1,
        "pageSize": 10,
        "sortColumn": "relevance",
        "sortDirection": "desc"
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code != 200:
            return []
        
        data = resp.json()
        results = []
        
        for hit in data.get("Results", []):
            results.append({
                "name": hit.get("Names", [{}])[0].get("Value", "") if hit.get("Names") else "",
                "crd_number": hit.get("CrdNumber", ""),
                "sec_number": hit.get("SecNumber", ""),
                "aum": hit.get("AUM"),
                "state": hit.get("State", ""),
                "has_disclosures": hit.get("HasDisclosure", False),
            })
        
        return results
    except Exception as e:
        print(f"Form ADV search error: {e}")
        return []


def get_form_adv_details(crd_number: str) -> Optional[FormADVInfo]:
    """
    Get detailed Form ADV info for an adviser by CRD number.
    """
    url = f"https://api.adviserinfo.sec.gov/IAPD/Content/Common/api/Firm/{crd_number}"
    
    headers = {"User-Agent": EDGAR_USER_AGENT}
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        
        # Extract AUM from form ADV data
        aum = None
        aum_date = None
        if "AUM" in data:
            aum = data.get("AUM")
            aum_date = data.get("AUMDate")
        
        # Get brochure URL
        brochure_url = None
        if data.get("HasBrochure"):
            brochure_url = f"https://adviserinfo.sec.gov/IAPD/Content/Common/api/Brochure?ProgramId=1&CrdNumber={crd_number}"
        
        return FormADVInfo(
            firm_name=data.get("Names", [{}])[0].get("Value", "") if data.get("Names") else "",
            crd_number=crd_number,
            sec_number=data.get("SecNumber", ""),
            aum=aum,
            aum_date=aum_date,
            employee_count=data.get("NumberOfEmployees"),
            state=data.get("State"),
            registration_status=data.get("RegistrationStatus", "Unknown"),
            has_disclosure_events=data.get("HasDisclosure", False),
            brochure_url=brochure_url,
        )
    except Exception as e:
        print(f"Form ADV details error: {e}")
        return None


def get_adv_for_firm(firm_name: str) -> Optional[FormADVInfo]:
    """
    Convenience function: search by name and get details for best match.
    """
    results = search_form_adv(firm_name)
    if not results:
        return None
    
    # Return first result (most relevant)
    best = results[0]
    if best.get("crd_number"):
        return get_form_adv_details(best["crd_number"])
    
    return None


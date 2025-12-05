"""Derived metrics with confidence-banded estimates."""

from datetime import date, timedelta
from dataclasses import dataclass


@dataclass
class FirmMetrics:
    # Tier 1: Direct from Form D
    fund_size: int              # dollars (max amount sold)
    lp_count: int               # from investor count
    first_close: date | None    # date of first sale
    
    # Tier 2: Derived estimates
    fund_age_months: int
    deployment_status: str      # "active" | "late" | "harvest"
    check_low: int              # conservative estimate
    check_mid: int              # base estimate  
    check_high: int             # aggressive estimate
    confidence: str             # "low" | "medium" | "high"
    
    # Activity
    filing_count: int
    days_since_last: int


def calculate_metrics(filings: list) -> FirmMetrics:
    """Calculate grounded estimates from Form D data."""
    
    if not filings:
        return FirmMetrics(0, 0, None, 0, "unknown", 0, 0, 0, "low", 0, 0)
    
    # --- Tier 1: Direct extraction ---
    
    # Fund size: max amount sold across all filings
    amounts = [f.total_amount_sold or f.total_offering_amount or 0 for f in filings]
    fund_size = max(amounts) if amounts else 0
    
    # LP count: max investor count
    lp_counts = [f.investor_count or 0 for f in filings]
    lp_count = max(lp_counts) if lp_counts else 0
    
    # First close: earliest date of first sale
    first_sales = [f.date_of_first_sale for f in filings if f.date_of_first_sale]
    first_close = min(first_sales) if first_sales else None
    
    # --- Tier 2: Derived with assumptions ---
    
    # Fund age
    if first_close:
        fund_age_months = (date.today() - first_close).days // 30
    else:
        # Fallback: use earliest filing date
        filing_dates = [f.filing_date for f in filings if f.filing_date]
        if filing_dates:
            fund_age_months = (date.today() - min(filing_dates)).days // 30
        else:
            fund_age_months = 0
    
    # Deployment status based on fund age
    if fund_age_months < 18:
        deployment_status = "active"
    elif fund_age_months < 42:
        deployment_status = "late"
    else:
        deployment_status = "harvest"
    
    # Check size estimation (the money calculation)
    check_low, check_mid, check_high, confidence = estimate_check_size(fund_size)
    
    # Activity metrics
    filing_count = len(filings)
    days_since_last = (date.today() - filings[0].filing_date).days if filings[0].filing_date else 0
    
    return FirmMetrics(
        fund_size=fund_size,
        lp_count=lp_count,
        first_close=first_close,
        fund_age_months=fund_age_months,
        deployment_status=deployment_status,
        check_low=check_low,
        check_mid=check_mid,
        check_high=check_high,
        confidence=confidence,
        filing_count=filing_count,
        days_since_last=days_since_last,
    )


def estimate_check_size(fund_size: int) -> tuple[int, int, int, str]:
    """
    Estimate check size range from fund size.
    
    Logic:
    - Reserve ratio by fund tier (45-55% for large funds)
    - Portfolio size estimate (25-45 companies)
    - Check = (Fund × (1 - Reserve)) / Portfolio
    """
    if fund_size < 1_000_000:  # < $1M, probably bad data
        return (0, 0, 0, "low")
    
    # Reserve ratios by fund size tier
    if fund_size < 50_000_000:       # <$50M seed fund
        reserve_low, reserve_high = 0.20, 0.30
        portfolio_low, portfolio_high = 15, 30
        confidence = "medium"
    elif fund_size < 150_000_000:    # $50-150M
        reserve_low, reserve_high = 0.30, 0.40
        portfolio_low, portfolio_high = 20, 40
        confidence = "medium"
    elif fund_size < 400_000_000:    # $150-400M
        reserve_low, reserve_high = 0.40, 0.50
        portfolio_low, portfolio_high = 25, 45
        confidence = "medium"
    else:                             # $400M+
        reserve_low, reserve_high = 0.45, 0.55
        portfolio_low, portfolio_high = 25, 50
        confidence = "medium"
    
    # Calculate range
    # Low estimate: high reserve, many companies
    deploy_low = fund_size * (1 - reserve_high)
    check_low = int(deploy_low / portfolio_high)
    
    # Mid estimate: average
    deploy_mid = fund_size * (1 - (reserve_low + reserve_high) / 2)
    check_mid = int(deploy_mid / ((portfolio_low + portfolio_high) / 2))
    
    # High estimate: low reserve, few companies
    deploy_high = fund_size * (1 - reserve_low)
    check_high = int(deploy_high / portfolio_low)
    
    return (check_low, check_mid, check_high, confidence)

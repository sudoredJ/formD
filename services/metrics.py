"""Derived metrics with confidence-banded estimates."""

from datetime import date
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
    
    # Extract Form D signals for check size estimation
    min_investments = [f.minimum_investment for f in filings if f.minimum_investment]
    min_investment = max(min_investments) if min_investments else 0
    
    # Calculate deployment percentage (amount sold vs target)
    offering_amounts = [f.total_offering_amount or 0 for f in filings]
    target_size = max(offering_amounts) if offering_amounts else fund_size
    pct_deployed = fund_size / target_size if target_size > 0 else 0.0
    
    check_low, check_mid, check_high, confidence = estimate_check_size(
        fund_size=fund_size,
        min_investment=min_investment,
        lp_count=lp_count,
        fund_age_months=fund_age_months,
        pct_deployed=pct_deployed,
    )
    
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


def estimate_check_size(
    fund_size: int,
    min_investment: int = 0,
    lp_count: int = 0,
    fund_age_months: int = 0,
    pct_deployed: float = 0.0,
) -> tuple[int, int, int, str]:
    """
    Estimate check size from Form D data.
    
    Formula: Check = (Fund Size × (1 - Reserve%)) / Portfolio Count
    
    Fund size is primary driver. Form D signals adjust to differentiate similar funds:
    - Min investment: institutional vs HNW LP base
    - LP count: spray vs concentrated
    - Fund age: early vs late deployment
    - Pct deployed: how much capital out the door
    """
    if fund_size < 1_000_000:
        return (0, 0, 0, "low")
    
    # Base portfolio count & reserve by fund size tier
    if fund_size < 25_000_000:          # Pre-seed
        portfolio_low, portfolio_high = 30, 50
        reserve = 0.25
    elif fund_size < 75_000_000:        # Seed
        portfolio_low, portfolio_high = 25, 40
        reserve = 0.40
    elif fund_size < 150_000_000:       # Large seed / Small A
        portfolio_low, portfolio_high = 20, 30
        reserve = 0.45
    elif fund_size < 300_000_000:       # Series A
        portfolio_low, portfolio_high = 15, 25
        reserve = 0.50
    else:                                # Growth
        portfolio_low, portfolio_high = 10, 20
        reserve = 0.55
    
    # Start at midpoint, then adjust based on Form D signals
    portfolio = (portfolio_low + portfolio_high) / 2
    signals = 0
    
    # Signal 1: Min investment (LP base structure)
    if min_investment >= 1_000_000:
        signals += 1
        # Institutional = disciplined, stays near midpoint
    elif min_investment > 0 and min_investment < 100_000:
        signals += 1
        portfolio -= 3  # HNW = often more concentrated
    
    # Signal 2: LP count relative to fund size
    if lp_count > 0:
        signals += 1
        avg_lp_check = fund_size / lp_count
        if avg_lp_check < 500_000:      # Many small LPs
            portfolio += 4               # Spray strategy
        elif avg_lp_check > 5_000_000:  # Few big anchors
            portfolio -= 3               # More concentrated
    
    # Signal 3: Fund age + deployment pace
    if fund_age_months > 0 and pct_deployed > 0:
        signals += 1
        monthly_rate = pct_deployed / fund_age_months
        
        if fund_age_months < 24:  # Young fund
            if monthly_rate > 0.03:     # >3%/mo = aggressive deployer
                portfolio += 4           # More deals, smaller checks
            elif monthly_rate < 0.015:  # <1.5%/mo = slow/concentrated
                portfolio -= 3
        else:  # Mature fund (2+ years)
            if pct_deployed > 0.7:      # >70% deployed = late stage
                reserve -= 0.05          # Less reserve left
            elif pct_deployed < 0.4:    # <40% deployed after 2yr = very slow
                portfolio -= 4           # Concentrated bets
    
    # Clamp to tier bounds
    portfolio = max(portfolio_low, min(portfolio_high, portfolio))
    
    deployable = fund_size * (1 - reserve)
    
    # Range based on THIS fund's adjusted portfolio
    check_mid = int(deployable / portfolio)
    check_low = int(check_mid * 0.75)
    check_high = int(check_mid * 1.35)
    
    confidence = "medium" if signals >= 1 else "low"
    
    return (check_low, check_mid, check_high, confidence)

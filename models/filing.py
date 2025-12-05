"""Form D filing model."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class FormDFiling:
    id: int
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
    created_at: datetime


"""Firm model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.db import query_db, execute_db


@dataclass
class Firm:
    id: int
    cik: str
    name: str
    sic_code: Optional[str]
    state: Optional[str]
    created_at: datetime
    updated_at: datetime


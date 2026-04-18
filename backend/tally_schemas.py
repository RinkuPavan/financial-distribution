from pydantic import BaseModel
from typing import List

class TallyTransactionEntry(BaseModel):
    """Single transaction entry for Tally"""
    month: str
    amount: int

class TallyDistributionResponse(BaseModel):
    """Tally-friendly response format"""
    status: str
    data: List[TallyTransactionEntry]
    total: int

# For backward compatibility, we'll also keep the original schema
class DistributionRequest(BaseModel):
    total_amount: int = 1000
    months: int = 12
    financial_year_start: str = "April"
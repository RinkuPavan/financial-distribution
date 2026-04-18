from pydantic import BaseModel, Field
from typing import Literal, List

class TransactionEntry(BaseModel):
    date: str  # YYYY-MM-DD format
    amount: int = Field(..., gt=0)

class MonthlyDistribution(BaseModel):
    month: str
    entries: List[TransactionEntry]

class DistributionRequest(BaseModel):
    total_amount: int = Field(..., gt=0)
    months: int = Field(..., gt=0)
    financial_year_start: Literal["April", "March"] = "April"

class DistributionResponse(BaseModel):
    monthly_distribution: List[MonthlyDistribution]

# Additional validation functions for use in service layer
def validate_date_spacing(entries: List[TransactionEntry], min_days: int = 5) -> bool:
    """
    Validate that dates are properly spaced (at least min_days apart).
    
    Args:
        entries: List of transaction entries
        min_days: Minimum number of days between dates
        
    Returns:
        True if dates are properly spaced, False otherwise
    """
    if len(entries) <= 1:
        return True
    
    # Parse dates and sort them
    parsed_dates = []
    for entry in entries:
        date_parts = entry.date.split('-')
        year, month, day = map(int, date_parts)
        parsed_dates.append((year, month, day))
    
    # Sort by date
    parsed_dates.sort()
    
    # Check spacing between dates
    for i in range(1, len(parsed_dates)):
        prev_year, prev_month, prev_day = parsed_dates[i-1]
        curr_year, curr_month, curr_day = parsed_dates[i]
        
        # Convert to datetime objects for difference calculation
        from datetime import date
        prev_date = date(prev_year, prev_month, prev_day)
        curr_date = date(curr_year, curr_month, curr_day)
        
        diff = (curr_date - prev_date).days
        if diff < min_days:
            return False
    
    return True

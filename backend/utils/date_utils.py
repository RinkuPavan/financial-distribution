import random
from datetime import date, timedelta
from typing import List

def generate_spaced_dates_int(year: int, month: int, num_dates: int = 3) -> List[int]:
    """
    Generate a list of valid spaced dates for a given month.
    
    Args:
        year: Year for the dates
        month: Month for the dates (1-12)
        num_dates: Number of dates to generate (3-4)
        
    Returns:
        List of valid date integers (between 4 and 26)
    """
    # Ensure we generate between 3 and 4 dates
    if num_dates < 3:
        num_dates = 3
    elif num_dates > 4:
        num_dates = 4
    
    max_attempts = 100  # Prevent infinite loops
    attempt = 0
    
    while attempt < max_attempts:
        # Generate candidate dates between 4 and 26
        candidates = []
        for _ in range(num_dates):
            candidate_date = random.randint(4, 26)
            candidates.append(candidate_date)
        
        # Sort the candidates
        candidates.sort()
        
        # Validate spacing (at least 5 days apart)
        valid_spacing = True
        for i in range(1, len(candidates)):
            if candidates[i] - candidates[i-1] < 5:
                valid_spacing = False
                break
        
        # If valid spacing, return the dates
        if valid_spacing:
            return candidates
        
        attempt += 1
    
    # If we couldn't generate valid dates after max_attempts, 
    # return sorted candidates (this is a fallback)
    return sorted(candidates)

def validate_date_spacing(entries: List[dict], min_days: int = 5) -> bool:
    """
    Validate that dates in entries are properly spaced.
    
    Args:
        entries: List of transaction entries with date strings
        min_days: Minimum number of days between dates
        
    Returns:
        True if dates are properly spaced, False otherwise
    """
    if len(entries) <= 1:
        return True
    
    # Parse dates and sort them
    parsed_dates = []
    for entry in entries:
        date_parts = entry["date"].split('-')
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

def generate_spaced_dates(year: int, month: int, num_dates: int = 3) -> List[str]:
    """
    Generate spaced dates as strings for a given month.
    
    Args:
        year: Year for the dates
        month: Month for the dates (1-12)
        num_dates: Number of dates to generate (3-4)
        
    Returns:
        List of date strings in YYYY-MM-DD format
    """
    # Generate integer dates
    int_dates = generate_spaced_dates_int(year, month, num_dates)
    
    # Convert to string format
    date_strings = []
    for day in int_dates:
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        date_strings.append(date_str)
    
    return date_strings
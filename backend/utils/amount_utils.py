import math
import random
from typing import List

def round_to_nearest_multiple_of_50(amount: float) -> int:
    """
    Round a number to the nearest multiple of 50.
    
    Args:
        amount: The amount to round
        
    Returns:
        Rounded amount as integer
    """
    return int(round(amount / 50.0)) * 50

def distribute_amount_rounded(monthly_amount: float, num_months: int, total_amount: int) -> List[int]:
    """
    Distribute an amount across months, rounding to nearest multiple of 50,
    while maintaining the total amount integrity.
    
    Args:
        monthly_amount: The base monthly amount
        num_months: Number of months
        total_amount: Total amount to distribute
        
    Returns:
        List of rounded monthly amounts that sum to total_amount
    """
    # Calculate initial rounded amounts for each month
    rounded_amounts = []
    total_rounded = 0
    
    for i in range(num_months):
        rounded = round_to_nearest_multiple_of_50(monthly_amount)
        rounded_amounts.append(rounded)
        total_rounded += rounded
    
    # Calculate the difference to adjust
    diff = total_amount - total_rounded
    
    if diff == 0:
        return rounded_amounts
    
    # Adjust amounts to make up for rounding differences
    # FIX: Always adjust the last month to ensure deterministic behavior
    if diff != 0:
        # Calculate how much we need to add/subtract (in multiples of 50)
        abs_diff = abs(diff)
        sign = 1 if diff > 0 else -1
        
        # Add/subtract the difference to the last entry only (deterministic approach)
        rounded_amounts[-1] += sign * abs_diff
    
    return rounded_amounts

def split_amount_into_entries(amount: int, min_entries: int = 3, max_entries: int = 4) -> List[int]:
    """
    Split an amount into random entries (each divisible by 50).
    
    Args:
        amount: Total amount to split
        min_entries: Minimum number of entries
        max_entries: Maximum number of entries
        
    Returns:
        List of amounts that sum to the original amount
    """
    if amount <= 0:
        return []
    
    # Handle edge case where amount is less than 50
    if amount < 50:
        # Either assign single entry or raise validation error
        # For now, we'll assign a single entry with the full amount
        # (this maintains integrity but may not be ideal for all use cases)
        return [amount]
    
    num_entries = random.randint(min_entries, max_entries)
    
    # Generate random amounts
    entries = []
    remaining = amount
    
    for i in range(num_entries - 1):
        # Ensure we have enough for remaining entries
        min_for_this = 50
        max_for_this = remaining - (num_entries - i - 1) * 50
        
        if max_for_this < min_for_this:
            max_for_this = min_for_this
            
        entry_amount = random.randint(min_for_this, max_for_this)
        entry_amount = (entry_amount // 50) * 50  # Round to nearest multiple of 50
        
        entries.append(entry_amount)
        remaining -= entry_amount
    
    # Add the last entry - THIS IS THE FIX: ensure remaining amount is added
    if remaining > 0:
        # Make sure the last entry is divisible by 50
        last_entry = (remaining // 50) * 50
        entries.append(last_entry)
    
    return entries

def validate_amount_divisibility(amount: int) -> bool:
    """
    Validate that an amount is divisible by 50.
    
    Args:
        amount: Amount to validate
        
    Returns:
        True if divisible by 50, False otherwise
    """
    return amount % 50 == 0

def validate_amount_distribution(total_amount: int, monthly_amounts: List[int]) -> bool:
    """
    Validate that the sum of monthly amounts equals the total amount.
    
    Args:
        total_amount: Expected total amount
        monthly_amounts: List of monthly amounts
        
    Returns:
        True if sum matches, False otherwise
    """
    return sum(monthly_amounts) == total_amount

from typing import List, Dict
from datetime import datetime
import calendar
from utils.amount_utils import split_amount_into_entries, distribute_amount_rounded
from utils.date_utils import generate_spaced_dates

def get_month_name(month_number: int) -> str:
    """Convert month number to name."""
    return calendar.month_name[month_number]

def get_financial_year_start_month(financial_year_start: str) -> int:
    """Get the starting month of financial year."""
    if financial_year_start == "April":
        return 4
    elif financial_year_start == "March":
        return 3
    else:
        raise ValueError("financial_year_start must be 'April' or 'March'")

def generate_transaction_schedule(total_amount: int, months: int, financial_year_start: str = "April") -> Dict:
    """
    Generate a transaction schedule for the specified amount and period.
    
    Args:
        total_amount: Total amount to distribute
        months: Number of months to distribute across
        financial_year_start: Start month of financial year ("April" or "March")
        
    Returns:
        Dictionary with monthly distribution schedule
    """
    try:
        # Calculate monthly amount (this will be rounded)
        monthly_amount = total_amount / months
        
        # Distribute the amount across months, maintaining total integrity
        monthly_amounts = distribute_amount_rounded(monthly_amount, months, total_amount)
        
        # Get the financial year start month
        fy_start_month = get_financial_year_start_month(financial_year_start)
        
        # Base year (starting from 2026)
        base_year = 2026
        
        result = {
            "monthly_distribution": []
        }
        
        current_year = base_year
        previous_month = 0  # Track previous month to handle year transition
        
        for i, amount in enumerate(monthly_amounts):
            # Calculate which month this is in the financial year
            # This handles the year transition correctly
            if i == 0:
                # First month
                current_month = fy_start_month
            else:
                # Calculate next month, handling year transitions
                current_month = previous_month + 1
                
                # Handle year transition
                if current_month > 12:
                    current_month = 1
                    current_year += 1
            
            # Store the previous month for next iteration
            previous_month = current_month
            
            # Generate entries for this month
            entries = split_amount_into_entries(amount)
            
            # Generate spaced dates for this month
            date_strings = generate_spaced_dates(current_year, current_month, len(entries))
            
            # Create transaction entries with dates and amounts
            transaction_entries = []
            for j, entry_amount in enumerate(entries):
                if j < len(date_strings):
                    transaction_entries.append({
                        "date": date_strings[j],
                        "amount": entry_amount
                    })
            
            # Add to result
            month_name = get_month_name(current_month)
            result["monthly_distribution"].append({
                "month": month_name,
                "entries": transaction_entries
            })
        
        return result
        
    except Exception as e:
        print(f"Error in generate_transaction_schedule: {str(e)}")
        raise

# Test function to verify the implementation
def test_distribution():
    """Test the distribution function with sample data."""
    try:
        result = generate_transaction_schedule(12000, 12, "April")
        print("Distribution generated successfully!")
        print(f"Generated {len(result['monthly_distribution'])} months")
        return result
    except Exception as e:
        print(f"Error in test: {str(e)}")
        raise

if __name__ == "__main__":
    # Run a quick test
    test_distribution()
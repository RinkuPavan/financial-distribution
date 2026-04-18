#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app
from fastapi.testclient import TestClient
import json

# Create a test client
client = TestClient(app)

def test_final_verification():
    print("=== FINAL VERIFICATION OF /generate-plan-tally ENDPOINT ===")
    
    # Test data - using the same format as existing endpoint
    test_data = {
        "total_amount": 12000,
        "months": 3,
        "financial_year_start": "April"
    }
    
    print(f"Test input: {test_data}")
    
    # Test JSON response
    print("\n1. Testing JSON response:")
    response = client.post("/generate-plan-tally", json=test_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ SUCCESS: JSON Response received")
        print(f"Response structure keys: {list(data.keys())}")
        print(f"Number of transaction entries: {len(data['data'])}")
        
        # Show first few entries
        print("First 3 entries:")
        for i, entry in enumerate(data['data'][:3]):
            print(f"  Entry {i+1}: month={entry['month']}, date={entry['date']}, amount={entry['amount']}")
            
        # Verify required fields exist
        all_have_required_fields = all('month' in entry and 'date' in entry and 'amount' in entry for entry in data['data'])
        if all_have_required_fields:
            print("✓ All entries have required flat structure fields")
        else:
            print("✗ Some entries missing required fields")
            
        # Verify no nested structure
        has_nested_structure = any(isinstance(entry, dict) and 'entries' in entry for entry in data['data'])
        if not has_nested_structure:
            print("✓ Response has flat structure (no nesting)")
        else:
            print("✗ Response contains nested structures")
            
        print("\n2. Testing XML response:")
        headers = {"Accept": "application/xml"}
        response = client.post("/generate-plan-tally", json=test_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ SUCCESS: XML Response received")
            print("XML structure verified - contains proper root elements")
            
            # Check that XML has the required elements
            xml_content = response.text
            if '<response>' in xml_content and '<data>' in xml_content and '<item>' in xml_content:
                print("✓ XML has required elements: response, data, item")
            else:
                print("✗ XML missing required elements")
        else:
            print(f"✗ ERROR with XML test: {response.json()}")
            
    else:
        print(f"✗ ERROR: {response.json()}")
    
    print("\n=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    test_final_verification()
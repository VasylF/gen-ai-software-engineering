#!/usr/bin/env python3
"""
Demo script for testing the Banking Transactions API
This script demonstrates all API endpoints and features
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Print a formatted API response"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2)}")
    except:
        print(f"Response:\n{response.text}")

def test_health():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_create_transactions():
    """Create sample transactions"""
    print("\n" + "="*60)
    print("🏦 CREATING SAMPLE TRANSACTIONS")
    print("="*60)
    
    transactions = [
        {
            "name": "Deposit to Account 1",
            "data": {
                "fromAccount": "ACC-00000",
                "toAccount": "ACC-12345",
                "amount": 1000.00,
                "currency": "USD",
                "type": "deposit"
            }
        },
        {
            "name": "Transfer 1",
            "data": {
                "fromAccount": "ACC-12345",
                "toAccount": "ACC-67890",
                "amount": 250.50,
                "currency": "USD",
                "type": "transfer"
            }
        },
        {
            "name": "Deposit to Account 2",
            "data": {
                "fromAccount": "ACC-00000",
                "toAccount": "ACC-67890",
                "amount": 500.25,
                "currency": "EUR",
                "type": "deposit"
            }
        },
        {
            "name": "Transfer 2",
            "data": {
                "fromAccount": "ACC-67890",
                "toAccount": "ACC-12345",
                "amount": 100.00,
                "currency": "USD",
                "type": "transfer"
            }
        },
        {
            "name": "Withdrawal",
            "data": {
                "fromAccount": "ACC-12345",
                "toAccount": "ACC-00000",
                "amount": 75.25,
                "currency": "USD",
                "type": "withdrawal"
            }
        }
    ]
    
    for trans in transactions:
        response = requests.post(
            f"{BASE_URL}/transactions",
            json=trans["data"],
            headers={"Content-Type": "application/json"}
        )
        print_response(trans["name"], response)

def test_get_all_transactions():
    """Get all transactions"""
    response = requests.get(f"{BASE_URL}/transactions")
    print_response("Get All Transactions", response)

def test_filter_by_account():
    """Filter transactions by account ID"""
    response = requests.get(f"{BASE_URL}/transactions?accountId=ACC-12345")
    print_response("Filter by Account (ACC-12345)", response)

def test_filter_by_type():
    """Filter transactions by type"""
    response = requests.get(f"{BASE_URL}/transactions?type=transfer")
    print_response("Filter by Type (transfer)", response)

def test_filter_by_date():
    """Filter transactions by date range"""
    today = datetime.now()
    from_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")
    
    response = requests.get(f"{BASE_URL}/transactions?from={from_date}&to={to_date}")
    print_response(f"Filter by Date Range ({from_date} to {to_date})", response)

def test_filter_combined():
    """Combine multiple filters"""
    response = requests.get(f"{BASE_URL}/transactions?accountId=ACC-12345&type=transfer")
    print_response("Combined Filters (Account + Type)", response)

def test_get_transaction_by_id():
    """Get a specific transaction by ID"""
    # First get all transactions to get an ID
    response = requests.get(f"{BASE_URL}/transactions")
    if response.status_code == 200:
        transactions = response.json()
        if transactions:
            trans_id = transactions[0]['id']
            response = requests.get(f"{BASE_URL}/transactions/{trans_id}")
            print_response(f"Get Transaction by ID ({trans_id})", response)

def test_get_account_balance():
    """Get account balance"""
    response = requests.get(f"{BASE_URL}/accounts/ACC-12345/balance")
    print_response("Get Account Balance (ACC-12345)", response)

def test_get_account_summary():
    """Get account summary (Task 4)"""
    response = requests.get(f"{BASE_URL}/accounts/ACC-12345/summary")
    print_response("Get Account Summary (ACC-12345)", response)

def test_validation_errors():
    """Test validation error handling"""
    print("\n" + "="*60)
    print("⚠️  TESTING VALIDATION ERRORS")
    print("="*60)
    
    test_cases = [
        {
            "name": "Invalid Amount (negative)",
            "data": {
                "fromAccount": "ACC-11111",
                "toAccount": "ACC-22222",
                "amount": -50,
                "currency": "USD",
                "type": "transfer"
            }
        },
        {
            "name": "Invalid Amount (too many decimals)",
            "data": {
                "fromAccount": "ACC-11111",
                "toAccount": "ACC-22222",
                "amount": 50.555,
                "currency": "USD",
                "type": "transfer"
            }
        },
        {
            "name": "Invalid Currency",
            "data": {
                "fromAccount": "ACC-11111",
                "toAccount": "ACC-22222",
                "amount": 50,
                "currency": "XXX",
                "type": "transfer"
            }
        },
        {
            "name": "Invalid Account Format",
            "data": {
                "fromAccount": "INVALID",
                "toAccount": "ACC-22222",
                "amount": 50,
                "currency": "USD",
                "type": "transfer"
            }
        },
        {
            "name": "Invalid Transaction Type",
            "data": {
                "fromAccount": "ACC-11111",
                "toAccount": "ACC-22222",
                "amount": 50,
                "currency": "USD",
                "type": "invalid"
            }
        },
        {
            "name": "Same From and To Account",
            "data": {
                "fromAccount": "ACC-11111",
                "toAccount": "ACC-11111",
                "amount": 50,
                "currency": "USD",
                "type": "transfer"
            }
        }
    ]
    
    for test in test_cases:
        response = requests.post(
            f"{BASE_URL}/transactions",
            json=test["data"],
            headers={"Content-Type": "application/json"}
        )
        print_response(test["name"], response)

def test_invalid_account_id():
    """Test invalid account ID format"""
    response = requests.get(f"{BASE_URL}/accounts/INVALID/balance")
    print_response("Get Balance with Invalid Account Format", response)

def test_nonexistent_transaction():
    """Test getting nonexistent transaction"""
    response = requests.get(f"{BASE_URL}/transactions/nonexistent-id")
    print_response("Get Nonexistent Transaction", response)

def main():
    """Run all tests"""
    print("\n")
    print("🏦  " + "="*56)
    print("    BANKING TRANSACTIONS API - DEMO & TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("="*60)
    
    # Check if API is running
    try:
        if not test_health():
            print("\n❌ API is not responding. Make sure the server is running!")
            print("   Run: python app.py")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API. Make sure the server is running!")
        print("   Run: python app.py")
        return
    
    print("✅ API is running!")
    
    # Run test suite
    test_create_transactions()
    test_get_all_transactions()
    test_filter_by_account()
    test_filter_by_type()
    test_filter_by_date()
    test_filter_combined()
    test_get_transaction_by_id()
    test_get_account_balance()
    test_get_account_summary()
    test_validation_errors()
    test_invalid_account_id()
    test_nonexistent_transaction()
    
    print("\n" + "="*60)
    print("✅ DEMO & TEST SUITE COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

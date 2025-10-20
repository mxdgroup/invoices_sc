#!/usr/bin/env python3
"""
Test script for Invoice Generator API
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_SECRET_TOKEN", "your-super-secret-token-here-change-this")
TEST_EMAIL = os.getenv("TEST_EMAIL", "test@example.com")

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_token():
    """Test token validation"""
    print("\n" + "="*60)
    print("Testing Token Validation")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(f"{API_URL}/test-token", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_generate_invoice():
    """Test invoice generation"""
    print("\n" + "="*60)
    print("Testing Invoice Generation")
    print("="*60)
    
    # Sample invoice data
    data = {
        "invoice": {
            "number": "00TI25-TEST001",
            "date_of_issuing": "March 6, 2025",
            "date_of_supply": "March 6, 2025"
        },
        "issued_to": {
            "name": "Test Customer",
            "address": "123 Test Street<br/>Test City, TC 12345",
            "trn": "TEST123456",
            "tel": "+1234567890",
            "email": TEST_EMAIL
        },
        "terms": {
            "payment_terms": "Payment on Delivery",
            "delivery_terms": "Ex-works Dubai"
        },
        "items": [
            {
                "description": "Test Item - Sample Product for Testing",
                "quantity": 2.0,
                "uom": "Pcs",
                "price_aed": 5000.00,
                "discount_pct": 10.0,
                "vat_pct": 5,
                "rate_usd": 3.6725
            },
            {
                "description": "Another Test Item - Second Product",
                "quantity": 1.0,
                "uom": "Pcs",
                "price_aed": 3000.00,
                "discount_pct": 0,
                "vat_pct": 5,
                "rate_usd": 3.6725
            }
        ],
        "supply_total_text": "Twelve thousand six hundred AED ONLY",
        "recipient_emails": [
            TEST_EMAIL  # Test email from environment variable
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("Sending request...")
    print(f"Invoice Number: {data['invoice']['number']}")
    print(f"Customer: {data['issued_to']['name']}")
    print(f"Items: {len(data['items'])}")
    print(f"Recipients: {', '.join(data['recipient_emails'])}")
    
    try:
        response = requests.post(
            f"{API_URL}/generate-invoice",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Success!")
            print(f"\nResponse:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print("✗ Failed!")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("INVOICE API TEST SUITE")
    print("="*60)
    print(f"API URL: {API_URL}")
    print(f"Token: {API_TOKEN[:10]}..." if len(API_TOKEN) > 10 else API_TOKEN)
    
    results = {
        "Health Check": test_health(),
        "Token Validation": test_token(),
        "Invoice Generation": test_generate_invoice()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


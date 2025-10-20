#!/usr/bin/env python3
"""
Test script for generating proforma invoices
"""
import requests
import json
import os
from pathlib import Path

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_SECRET_TOKEN", "your-super-secret-token-here-change-this")

def test_proforma_invoice():
    """Test proforma invoice generation"""
    
    # Load sample data
    sample_file = Path(__file__).parent / "sample_proforma_request.json"
    with open(sample_file, 'r') as f:
        data = json.load(f)
    
    print("🔍 Testing Proforma Invoice Generation")
    print(f"   API URL: {API_URL}")
    print(f"   Invoice Number: {data['invoice']['number']}")
    print(f"   Customer: {data['issued_to']['name']}")
    print(f"   Items: {len(data['items'])}")
    print()
    
    # Make request
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("📤 Sending request...")
    response = requests.post(
        f"{API_URL}/generate-proforma-invoice",
        headers=headers,
        json=data
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS!")
        print(f"   Invoice: {result['invoice_number']}")
        print(f"   PDF File: {result['pdf_filename']}")
        print(f"   PDF Size: {result['pdf_size_kb']} KB")
        print(f"   Total: {result['total_aed']} AED")
        print(f"   Sent to: {', '.join(result['emails_sent_to'])}")
        return True
    else:
        print("❌ FAILED!")
        try:
            error = response.json()
            print(f"   Error: {error.get('detail', 'Unknown error')}")
        except:
            print(f"   Response: {response.text}")
        return False

if __name__ == "__main__":
    success = test_proforma_invoice()
    exit(0 if success else 1)


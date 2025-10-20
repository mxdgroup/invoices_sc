#!/bin/bash
# cURL Examples for Invoice Generator API

# Configuration
API_URL="http://localhost:8000"  # Change to your production URL
TOKEN="your-secret-token-here"    # Change to your actual token

echo "Invoice Generator API - cURL Examples"
echo "========================================"
echo ""

# 1. Health Check
echo "1. Health Check"
echo "Command:"
echo "curl $API_URL/health"
echo ""
read -p "Press Enter to run..."
curl $API_URL/health
echo ""
echo ""

# 2. Test Token
echo "2. Test Token Validation"
echo "Command:"
echo "curl -X POST $API_URL/test-token -H \"Authorization: Bearer $TOKEN\""
echo ""
read -p "Press Enter to run..."
curl -X POST $API_URL/test-token \
  -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

# 3. Generate Invoice
echo "3. Generate Invoice (from sample file)"
echo "Command:"
cat << 'EOF'
curl -X POST $API_URL/generate-invoice \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @sample_request.json
EOF
echo ""
read -p "Press Enter to run..."
curl -X POST $API_URL/generate-invoice \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @sample_request.json
echo ""
echo ""

# 4. Generate Invoice (inline JSON)
echo "4. Generate Invoice (inline minimal example)"
echo "Command:"
cat << 'EOF'
curl -X POST $API_URL/generate-invoice \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": {
      "number": "TEST-001",
      "date_of_issuing": "March 6, 2025",
      "date_of_supply": "March 6, 2025"
    },
    "issued_to": {
      "name": "Test Customer",
      "address": "123 Test St",
      "email": "test@example.com"
    },
    "terms": {
      "payment_terms": "Payment on Delivery"
    },
    "items": [{
      "description": "Test Item",
      "quantity": 1.0,
      "uom": "Pcs",
      "price_aed": 1000.00,
      "discount_pct": 0,
      "vat_pct": 5,
      "rate_usd": 3.6725
    }],
    "supply_total_text": "One thousand AED ONLY",
    "recipient_emails": ["test@example.com"]
  }'
EOF
echo ""
read -p "Press Enter to run..."
curl -X POST $API_URL/generate-invoice \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": {
      "number": "TEST-001",
      "date_of_issuing": "March 6, 2025",
      "date_of_supply": "March 6, 2025"
    },
    "issued_to": {
      "name": "Test Customer",
      "address": "123 Test St",
      "email": "test@example.com"
    },
    "terms": {
      "payment_terms": "Payment on Delivery"
    },
    "items": [{
      "description": "Test Item",
      "quantity": 1.0,
      "uom": "Pcs",
      "price_aed": 1000.00,
      "discount_pct": 0,
      "vat_pct": 5,
      "rate_usd": 3.6725
    }],
    "supply_total_text": "One thousand AED ONLY",
    "recipient_emails": ["test@example.com"]
  }'
echo ""
echo ""

echo "========================================"
echo "All examples completed!"
echo ""
echo "To use these commands directly:"
echo "1. Edit this file and update API_URL and TOKEN"
echo "2. Run: ./curl_examples.sh"


# Proforma Invoice API - Request Examples

## 📡 Endpoint

```
POST http://localhost:8000/generate-proforma-invoice
```

**Authentication Required**: Yes (Bearer token in Authorization header)

---

## 📋 JSON Structure

### Complete Example

```json
{
  "invoice": {
    "number": "00PI25-00000003",
    "date_of_issuing": "October 20, 2025"
  },
  "issued_to": {
    "name": "John Smith",
    "address": "123 Main Street, Apartment 4B, New York, NY, 10001, USA",
    "trn": "",
    "email": "john.smith@example.com"
  },
  "terms": {
    "payment_terms": "Advance payment of 50% before Delivery"
  },
  "items": [
    {
      "description": "Diamond Ring 18K White Gold, 1.5ct Solitaire",
      "sub_description": "GIA Certified, D-VVS1, SKU: DR-18K-150",
      "quantity": 1.0,
      "uom": "Pcs",
      "price_incl_vat_aed": 25000.00,
      "discount_pct": 15,
      "vat_pct": 5
    },
    {
      "description": "Pearl Necklace, 18K Yellow Gold, AAA+ Grade Pearls",
      "sub_description": "",
      "quantity": 2.0,
      "uom": "Pcs",
      "price_incl_vat_aed": 8500.00,
      "discount_pct": 10,
      "vat_pct": 5
    }
  ],
  "amount_in_words": "Forty seven thousand one hundred AED ONLY",
  "recipient_emails": [
    "john.smith@example.com"
  ]
}
```

---

## 🔑 Field Descriptions

### `invoice` (Required)
Invoice metadata

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `number` | string | ✅ Yes | Proforma invoice number | "00PI25-00000003" |
| `date_of_issuing` | string | ✅ Yes | Issue date in readable format | "October 20, 2025" |

### `issued_to` (Required)
Customer/recipient information

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `name` | string | ✅ Yes | Customer name or company | "John Smith" |
| `address` | string | ✅ Yes | Full billing address | "123 Main St, NY, 10001" |
| `trn` | string | ❌ No | Tax Registration Number (can be empty) | "" or "123456789" |
| `email` | string | ✅ Yes | Customer email address | "john@example.com" |

### `terms` (Required)
Payment terms and conditions

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `payment_terms` | string | ✅ Yes | Payment conditions | "Advance payment of 50% before Delivery" |

### `items` (Required)
Array of products/services

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `description` | string | ✅ Yes | Main product description | "Diamond Ring 18K White Gold" |
| `sub_description` | string | ❌ No | Additional details or SKU | "GIA Certified, D-VVS1" |
| `quantity` | number | ✅ Yes | Quantity (supports decimals) | 1.0 or 2.5 |
| `uom` | string | ✅ Yes | Unit of measure | "Pcs", "Kg", "Units" |
| `price_incl_vat_aed` | number | ✅ Yes | **Price INCLUDING VAT** in AED | 25000.00 |
| `discount_pct` | number | ❌ No | Discount percentage (0-100) | 15 |
| `vat_pct` | number | ❌ No | VAT percentage (default: 5) | 5 |

**Important**: `price_incl_vat_aed` is the price **WITH VAT INCLUDED** (different from tax invoices)

### Other Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `amount_in_words` | string | ✅ Yes | Total amount in words | "Forty seven thousand AED ONLY" |
| `recipient_emails` | array | ✅ Yes | List of email addresses to send PDF to | ["email1@example.com", "email2@example.com"] |

---

## 🌐 cURL Examples

### Basic Request

```bash
curl -X POST "http://localhost:8000/generate-proforma-invoice" \
  -H "Authorization: Bearer your-super-secret-token-here-change-this" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": {
      "number": "00PI25-00000003",
      "date_of_issuing": "October 20, 2025"
    },
    "issued_to": {
      "name": "John Smith",
      "address": "123 Main Street, New York, NY, 10001",
      "trn": "",
      "email": "john.smith@example.com"
    },
    "terms": {
      "payment_terms": "Advance payment of 50% before Delivery"
    },
    "items": [
      {
        "description": "Diamond Ring 18K White Gold",
        "sub_description": "GIA Certified",
        "quantity": 1.0,
        "uom": "Pcs",
        "price_incl_vat_aed": 25000.00,
        "discount_pct": 15,
        "vat_pct": 5
      }
    ],
    "amount_in_words": "Twenty one thousand two hundred fifty AED ONLY",
    "recipient_emails": ["john.smith@example.com"]
  }'
```

### Using JSON File

```bash
curl -X POST "http://localhost:8000/generate-proforma-invoice" \
  -H "Authorization: Bearer your-super-secret-token-here-change-this" \
  -H "Content-Type: application/json" \
  -d @proforma_request_example.json
```

### Production Server

```bash
curl -X POST "https://your-server.com/generate-proforma-invoice" \
  -H "Authorization: Bearer your-actual-production-token" \
  -H "Content-Type: application/json" \
  -d @proforma_request_example.json
```

---

## 🐍 Python Examples

### Using `requests` Library

```python
import requests

url = "http://localhost:8000/generate-proforma-invoice"
headers = {
    "Authorization": "Bearer your-super-secret-token-here-change-this",
    "Content-Type": "application/json"
}

data = {
    "invoice": {
        "number": "00PI25-00000003",
        "date_of_issuing": "October 20, 2025"
    },
    "issued_to": {
        "name": "John Smith",
        "address": "123 Main Street, New York, NY, 10001",
        "trn": "",
        "email": "john.smith@example.com"
    },
    "terms": {
        "payment_terms": "Advance payment of 50% before Delivery"
    },
    "items": [
        {
            "description": "Diamond Ring 18K White Gold, 1.5ct",
            "sub_description": "GIA Certified, D-VVS1",
            "quantity": 1.0,
            "uom": "Pcs",
            "price_incl_vat_aed": 25000.00,
            "discount_pct": 15,
            "vat_pct": 5
        }
    ],
    "amount_in_words": "Twenty one thousand two hundred fifty AED ONLY",
    "recipient_emails": ["john.smith@example.com"]
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print("✅ Success!")
    print(f"Invoice: {result['invoice_number']}")
    print(f"PDF: {result['pdf_filename']}")
    print(f"Size: {result['pdf_size_kb']} KB")
    print(f"Total: {result['total_aed']} AED")
    print(f"Sent to: {', '.join(result['emails_sent_to'])}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())
```

### Using JSON File

```python
import requests
import json

url = "http://localhost:8000/generate-proforma-invoice"
headers = {
    "Authorization": "Bearer your-super-secret-token-here-change-this",
    "Content-Type": "application/json"
}

# Load from file
with open('proforma_request_example.json', 'r') as f:
    data = json.load(f)

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### With Error Handling

```python
import requests
import json

def generate_proforma_invoice(invoice_data, api_token):
    """Generate proforma invoice via API"""
    
    url = "http://localhost:8000/generate-proforma-invoice"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=invoice_data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Invoice {result['invoice_number']} generated successfully!")
        print(f"   PDF: {result['pdf_filename']}")
        print(f"   Size: {result['pdf_size_kb']} KB")
        print(f"   Sent to: {', '.join(result['emails_sent_to'])}")
        
        return result
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response is not None:
            print(f"   Detail: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to server")
    except requests.exceptions.Timeout:
        print("❌ Timeout: Request took too long")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

# Usage
invoice_data = {
    "invoice": {"number": "00PI25-00000003", "date_of_issuing": "October 20, 2025"},
    "issued_to": {
        "name": "John Smith",
        "address": "123 Main St, NY",
        "trn": "",
        "email": "john@example.com"
    },
    "terms": {"payment_terms": "Advance payment of 50% before Delivery"},
    "items": [{
        "description": "Diamond Ring",
        "sub_description": "",
        "quantity": 1.0,
        "uom": "Pcs",
        "price_incl_vat_aed": 25000.00,
        "discount_pct": 15,
        "vat_pct": 5
    }],
    "amount_in_words": "Twenty one thousand two hundred fifty AED ONLY",
    "recipient_emails": ["john@example.com"]
}

generate_proforma_invoice(invoice_data, "your-api-token")
```

---

## 📤 Response Format

### Success Response (200 OK)

```json
{
  "status": "success",
  "message": "Proforma invoice generated and sent successfully",
  "invoice_number": "00PI25-00000003",
  "pdf_filename": "ProformaInvoice_00PI25-00000003.pdf",
  "pdf_size_kb": 789.6,
  "emails_sent_to": [
    "john.smith@example.com"
  ],
  "total_aed": "47,100.00"
}
```

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 🧪 Test with the Included Script

```bash
cd /home/kali/pdf_script/fast_api_invoice_server

# Edit test_proforma.py if needed to set correct token
python test_proforma.py
```

---

## ⚠️ Important Notes

### 1. **Price Includes VAT**
Unlike tax invoices, the `price_incl_vat_aed` field is the price **WITH VAT ALREADY INCLUDED**.

**Example:**
- If final price should be 1,050 AED (including 5% VAT)
- Set `price_incl_vat_aed: 1050.00`
- The system will back-calculate: 1,000 AED (excl. VAT) + 50 AED (VAT)

### 2. **Multiple Recipients**
You can send the invoice to multiple email addresses:
```json
"recipient_emails": [
  "customer@example.com",
  "accounting@yourcompany.com",
  "manager@yourcompany.com"
]
```

### 3. **Discount Calculation**
Discount is applied to the gross amount (price × quantity) before VAT calculation.

### 4. **Amount in Words**
Must match the calculated total. Use proper formatting:
- "Twenty one thousand two hundred fifty AED ONLY"
- "Forty seven thousand one hundred AED ONLY"

### 5. **Empty Fields**
Optional fields can be empty strings but must be present:
```json
"trn": "",
"sub_description": ""
```

---

## 📋 Quick Reference

### Minimum Required Fields

```json
{
  "invoice": {
    "number": "REQUIRED",
    "date_of_issuing": "REQUIRED"
  },
  "issued_to": {
    "name": "REQUIRED",
    "address": "REQUIRED",
    "trn": "",
    "email": "REQUIRED"
  },
  "terms": {
    "payment_terms": "REQUIRED"
  },
  "items": [
    {
      "description": "REQUIRED",
      "sub_description": "",
      "quantity": 1.0,
      "uom": "REQUIRED",
      "price_incl_vat_aed": 0.00,
      "discount_pct": 0,
      "vat_pct": 5
    }
  ],
  "amount_in_words": "REQUIRED",
  "recipient_emails": ["REQUIRED"]
}
```

---

## 🔐 Authentication

### Get Your Token
Token is set in the server's `.env` file:
```
API_SECRET_TOKEN=your-super-secret-token-here-change-this
```

### Use in Request
```bash
Authorization: Bearer your-super-secret-token-here-change-this
```

---

## 📚 Additional Examples

See these files for more examples:
- `sample_proforma_request.json` - 2 items example
- `proforma_request_example.json` - 3 items example
- `test_proforma.py` - Python test script

---

**Need Help?** Check `PROFORMA_INVOICE_USAGE.md` for detailed documentation.


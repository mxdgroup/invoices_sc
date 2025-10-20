# Proforma Invoice Setup - Summary

## ✅ What Was Done

I've successfully set up the proforma invoice generation system based on your HTML template. Here's what was created:

### 1. **New Files Created**

#### `/home/kali/pdf_script/generate_proforma_invoice.py`
- Core logic for generating proforma invoice HTML from JSON data
- Handles VAT-inclusive pricing calculations
- Automatically calculates:
  - Total discount
  - Total excluding VAT
  - Total VAT amount
  - Total including VAT
  - Advance payment (50% of total)

#### `/home/kali/pdf_script/fast_api_invoice_server/sample_proforma_request.json`
- Sample request based on your HTML template (Invoice #00PI25-00000002)
- Shows the exact JSON structure needed
- Ready to use for testing

#### `/home/kali/pdf_script/fast_api_invoice_server/PROFORMA_INVOICE_USAGE.md`
- Complete documentation for the proforma invoice feature
- Includes field descriptions, examples, and calculation logic
- Shows differences between tax invoices and proforma invoices

#### `/home/kali/pdf_script/fast_api_invoice_server/test_proforma.py`
- Test script for easy testing
- Usage: `python test_proforma.py`

### 2. **Modified Files**

#### `main.py`
- Added import for `generate_proforma_invoice` module
- Created new Pydantic models for proforma invoices:
  - `ProformaInvoiceInfo`
  - `ProformaIssuedTo`
  - `ProformaTerms`
  - `ProformaItem`
  - `ProformaInvoiceRequest`
- Added new endpoint: `/generate-proforma-invoice`

#### `README.md`
- Updated features list
- Added proforma invoice endpoint documentation

---

## 🎯 Key Differences: Tax Invoice vs Proforma Invoice

| Aspect | Tax Invoice | Proforma Invoice |
|--------|-------------|------------------|
| **Endpoint** | `/generate-invoice` | `/generate-proforma-invoice` |
| **Purpose** | Official tax document | Quotation/estimate |
| **Price Type** | Excludes VAT | **Includes VAT** |
| **TRN** | Required | Optional (blank) |
| **Date Fields** | Issue date + Supply date | Issue date only |
| **Columns** | 12 columns (with USD) | 9 columns (AED only) |
| **Footer** | Released + Received | Released + Stamp |
| **Advance** | Not shown | Shows 50% advance |

---

## 🚀 How to Use

### 1. Start the Server

```bash
cd /home/kali/pdf_script/fast_api_invoice_server
python main.py
```

### 2. Test the Proforma Invoice

#### Option A: Using the test script
```bash
python test_proforma.py
```

#### Option B: Using cURL
```bash
curl -X POST "http://localhost:8000/generate-proforma-invoice" \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d @sample_proforma_request.json
```

### 3. Sample Request Structure

```json
{
  "invoice": {
    "number": "00PI25-00000002",
    "date_of_issuing": "October 12, 2025"
  },
  "issued_to": {
    "name": "Customer Name",
    "address": "Full address",
    "trn": "",
    "email": "customer@example.com"
  },
  "terms": {
    "payment_terms": "Advance payment of 50% before Delivery"
  },
  "items": [
    {
      "description": "Product name",
      "sub_description": "Optional SKU or details",
      "quantity": 1.0,
      "uom": "Pcs",
      "price_incl_vat_aed": 36493.00,
      "discount_pct": 20,
      "vat_pct": 5
    }
  ],
  "amount_in_words": "Total in words",
  "recipient_emails": ["customer@example.com"]
}
```

---

## 📊 Example Calculation

Given:
- Price (Incl. VAT): 36,493.00 AED
- Quantity: 1
- Discount: 20%
- VAT: 5%

Calculation:
1. **Gross** = 36,493.00 × 1 = 36,493.00
2. **Discount** = 36,493.00 × 20% = 7,298.60
3. **Amount (Incl. VAT)** = 36,493.00 - 7,298.60 = 29,194.40
4. **Amount (Excl. VAT)** = 29,194.40 / 1.05 = 27,804.19
5. **VAT Amount** = 29,194.40 - 27,804.19 = 1,390.21

---

## ✅ Verification Checklist

- [x] Proforma invoice generator created
- [x] FastAPI endpoint added
- [x] Pydantic models defined
- [x] Sample request JSON created
- [x] Documentation written
- [x] Test script created
- [x] README updated
- [x] No syntax errors
- [x] Follows same pattern as tax invoice

---

## 🎨 HTML Template Used

The generated HTML matches your template:
- ✅ Header with "PROFORMA INVOICE" title
- ✅ Invoice number and date
- ✅ Logo placeholder
- ✅ Issued By / Bill To grid
- ✅ Bank Details / Terms grid
- ✅ Items table with 9 columns
- ✅ "Amount in Words" row
- ✅ Totals table (right-aligned)
- ✅ Terms and conditions with advance payment
- ✅ Released By section with signature/stamp areas
- ✅ All styling from your original HTML

---

## 🔄 Next Steps

1. **Test locally**: Run `python test_proforma.py` to generate a test invoice
2. **Customize**: Edit company details in `generate_proforma_invoice.py` if needed
3. **Deploy**: Follow the same deployment process as the tax invoice API
4. **Monitor**: Check logs for any issues: `journalctl -u invoice-api -f`

---

## 📞 Support

- See `PROFORMA_INVOICE_USAGE.md` for detailed usage
- Check `sample_proforma_request.json` for examples
- Run `test_proforma.py` for quick testing

**Everything is ready to generate proforma invoices!** 🎉


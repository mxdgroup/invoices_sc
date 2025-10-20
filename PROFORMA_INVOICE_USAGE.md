# Proforma Invoice Generation

This document explains how to generate **Proforma Invoices** using the FastAPI Invoice Server.

## Overview

The system now supports two types of invoices:
1. **Tax Invoice** (endpoint: `/generate-invoice`) - Standard tax invoice with detailed pricing
2. **Proforma Invoice** (endpoint: `/generate-proforma-invoice`) - Pre-invoice for quotations

## Key Differences: Tax Invoice vs Proforma Invoice

| Feature | Tax Invoice | Proforma Invoice |
|---------|-------------|------------------|
| Purpose | Official tax document | Quotation/estimate |
| TRN | Required | Optional (blank) |
| Pricing | Price excludes VAT | Price includes VAT |
| Date Fields | Date of Issuing + Date of Supply | Date of Issuing only |
| Columns | 12 columns (includes USD) | 9 columns (AED only) |
| Footer | Released By + Received By | Released By + Stamp |
| Advance Payment | Not shown | Shows 50% advance |

## Endpoint

```
POST /generate-proforma-invoice
```

**Authentication:** Requires `Authorization` header with your API secret token

## Request Format

```json
{
  "invoice": {
    "number": "00PI25-00000002",
    "date_of_issuing": "October 12, 2025"
  },
  "issued_to": {
    "name": "Customer Name",
    "address": "Full customer address",
    "trn": "",
    "email": "customer@example.com"
  },
  "terms": {
    "payment_terms": "Advance payment of 50% before Delivery"
  },
  "items": [
    {
      "description": "Product description",
      "sub_description": "Optional sub-description or SKU",
      "quantity": 1.0,
      "uom": "Pcs",
      "price_incl_vat_aed": 36493.00,
      "discount_pct": 20,
      "vat_pct": 5
    }
  ],
  "amount_in_words": "Thirty seven thousand nine hundred twenty AED ONLY",
  "recipient_emails": [
    "customer@example.com"
  ]
}
```

## Field Descriptions

### invoice
- `number`: Proforma invoice number (e.g., "00PI25-00000002")
- `date_of_issuing`: Issue date in readable format (e.g., "October 12, 2025")

### issued_to
- `name`: Customer/company name
- `address`: Full billing address
- `trn`: Tax Registration Number (optional, leave empty for proforma)
- `email`: Customer email address

### terms
- `payment_terms`: Payment conditions (e.g., "Advance payment of 50% before Delivery")

### items (array)
- `description`: Main product description
- `sub_description`: Optional additional details or SKU
- `quantity`: Quantity (supports decimals)
- `uom`: Unit of measure (e.g., "Pcs", "Units", "Kg")
- `price_incl_vat_aed`: Unit price **including VAT** in AED
- `discount_pct`: Discount percentage (0-100)
- `vat_pct`: VAT percentage (typically 5 in UAE)

### Other Fields
- `amount_in_words`: Total amount written in words (e.g., "Thirty seven thousand nine hundred twenty AED ONLY")
- `recipient_emails`: Array of email addresses to send the invoice to

## Example cURL Request

```bash
curl -X POST "http://localhost:8000/generate-proforma-invoice" \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d @sample_proforma_request.json
```

## Response Format

```json
{
  "status": "success",
  "message": "Proforma invoice generated and sent successfully",
  "invoice_number": "00PI25-00000002",
  "pdf_filename": "ProformaInvoice_00PI25-00000002.pdf",
  "pdf_size_kb": 45.23,
  "emails_sent_to": [
    "customer@example.com"
  ],
  "total_aed": "37,920.00"
}
```

## Calculation Logic

The proforma invoice uses **VAT-inclusive pricing**:

1. **Gross Amount** = `price_incl_vat_aed × quantity`
2. **Discount Amount** = `gross × (discount_pct / 100)`
3. **Line Total (Incl. VAT)** = `gross - discount`
4. **Line Total (Excl. VAT)** = `line_total / (1 + vat_pct/100)`
5. **VAT Amount** = `line_total_incl - line_total_excl`

The system automatically calculates:
- Total Discount
- Total (Excl. VAT)
- Total VAT
- Total (Incl. VAT)
- Advance Payment (50% of total)

## Testing

Use the sample request file:

```bash
# Test with the sample proforma invoice
curl -X POST "http://localhost:8000/generate-proforma-invoice" \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d @sample_proforma_request.json
```

## Notes

1. **Price Format**: Prices in proforma invoices **include VAT**, unlike tax invoices where prices exclude VAT
2. **TRN Field**: Can be left empty for proforma invoices
3. **Advance Payment**: Automatically calculated as 50% of the total amount
4. **Email**: PDF is automatically sent to all addresses in `recipient_emails`
5. **File Naming**: PDFs are named `ProformaInvoice_{invoice_number}.pdf`

## Common Use Cases

- **Quotations**: Send to customers before confirming an order
- **Estimates**: Provide pricing information without creating a tax document
- **Pre-orders**: Show advance payment requirements
- **International Orders**: Provide pricing before formal invoicing


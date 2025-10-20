# Invoice Generator API - Summary

## 📋 What This Does

- **Receives**: JSON invoice data via POST request
- **Generates**: Professional PDF invoice (named by invoice number)
- **Sends**: PDF via email using Resend to multiple recipients
- **Security**: Token-based authentication

## 🔑 Key Features

✅ **Secure API** - Token authentication required
✅ **Dynamic PDF naming** - Files named by invoice number (e.g., `Invoice_00TI25-00000011.pdf`)
✅ **Multiple recipients** - Send to customer + CC internal emails
✅ **Auto-calculations** - Discounts, VAT, totals calculated automatically
✅ **Hardcoded company info** - No need to send company details in JSON
✅ **Production ready** - Systemd service, Nginx config included

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application (main server) |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variables template |
| `sample_request.json` | Example invoice JSON |
| `test_api.py` | Test script |
| `start.sh` | Local development startup |
| `invoice-api.service` | Systemd service for production |
| `README.md` | Full documentation |
| `QUICKSTART.md` | Quick start guide |

## 🔌 API Endpoint

### POST `/generate-invoice`

**Headers:**
```
Authorization: Bearer your-secret-token
Content-Type: application/json
```

**Request Body:**
```json
{
  "invoice": {
    "number": "00TI25-00000011",
    "date_of_issuing": "March 6, 2025",
    "date_of_supply": "March 6, 2025"
  },
  "issued_to": {
    "name": "Customer Name",
    "address": "Address",
    "email": "customer@example.com"
  },
  "terms": {
    "payment_terms": "Payment on Delivery"
  },
  "items": [{
    "description": "Item",
    "quantity": 1.0,
    "uom": "Pcs",
    "price_aed": 1000.00,
    "discount_pct": 0,
    "vat_pct": 5,
    "rate_usd": 3.6725
  }],
  "supply_total_text": "One thousand AED ONLY",
  "recipient_emails": ["customer@example.com"]
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Invoice generated and sent successfully",
  "invoice_number": "00TI25-00000011",
  "pdf_filename": "Invoice_00TI25-00000011.pdf",
  "pdf_size_kb": 17.4,
  "emails_sent_to": ["customer@example.com"],
  "total_aed": "220,304.83",
  "total_usd": "59,984.70"
}
```

## ⚙️ Environment Variables

Required in `.env` file:

```env
API_SECRET_TOKEN=your-super-secret-token
RESEND_API_KEY=re_your_resend_api_key
FROM_EMAIL=invoices@yourdomain.com
```

## 🚀 Quick Commands

### Local Development
```bash
./start.sh
```

### Test
```bash
export API_SECRET_TOKEN=your-token
./test_api.py
```

### Production Deploy
```bash
# Copy files to server
scp -r . root@server:/var/www/invoice-api/fast_api_invoice_server/

# On server
systemctl start invoice-api
systemctl enable invoice-api
```

## 🔐 Security Notes

- Token should be 32+ random characters
- Store `.env` securely (never commit to git)
- Always use HTTPS in production
- Rate limit in production (via nginx or middleware)

## 📊 Flow

```
1. Client sends JSON + token to API
        ↓
2. API validates token
        ↓
3. Generate HTML from JSON
        ↓
4. Convert HTML to PDF
        ↓
5. Name PDF by invoice number
        ↓
6. Send PDF via Resend to recipients
        ↓
7. Return success response
```

## 🌐 Production URLs

- **API**: `https://your-domain.com/generate-invoice`
- **Health**: `https://your-domain.com/health`
- **Test Token**: `https://your-domain.com/test-token`

## 📝 What's NOT in JSON (Hardcoded)

These are hardcoded in `main.py` (via parent directory's `generate_invoice.py`):

- Company name: SUZANNE CODE JEWELLERY TRADING L.L.C.
- Company address
- Company TRN, phone, email
- Bank details (IBAN, SWIFT, etc.)
- Company logo

This means you only send variable data (customer, items, etc.) in the JSON!

## 💡 Tips

- Keep invoices consistent by using sequential invoice numbers
- Add your own email to `recipient_emails` for records
- Monitor logs: `journalctl -u invoice-api -f`
- Test locally before deploying to production
- Backup `.env` file securely

## 🆘 Support Endpoints

- `GET /` - Basic health check
- `GET /health` - Detailed health with config status
- `POST /test-token` - Verify your token works

---

**Ready for deployment!** 🚀


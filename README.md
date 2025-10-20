# Invoice Generator API Server

FastAPI server for generating PDF invoices and sending them via email using Resend.

## 🚀 Features

- **Secure API**: Token-based authentication
- **PDF Generation**: Automatic PDF creation from JSON data
- **Email Delivery**: Send invoices via Resend to multiple recipients
- **Auto-naming**: PDF files named by invoice number
- **Company Info**: Hardcoded company details (no need in JSON)
- **Dual Invoice Types**: Support for both Tax Invoices and Proforma Invoices

## 📦 Installation

### 1. Install Dependencies

```bash
cd fast_api_invoice_server
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
nano .env
```

Edit `.env` with your values:

```env
API_SECRET_TOKEN=your-super-secret-token-here
RESEND_API_KEY=re_your_resend_api_key
FROM_EMAIL=invoices@yourdomain.com
```

**Get Resend API Key**: Sign up at [resend.com](https://resend.com) and create an API key.

### 3. Load Environment Variables

```bash
export $(cat .env | xargs)
```

Or use `python-dotenv`:
```bash
pip install python-dotenv
```

## 🏃 Running the Server

### Development

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production (Hetzner)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use gunicorn:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📡 API Endpoints

### Health Check

```bash
GET /
GET /health
```

### Test Token

```bash
POST /test-token
Headers: Authorization: Bearer your-secret-token
```

### Generate Tax Invoice

```bash
POST /generate-invoice
Headers: 
  Authorization: Bearer your-secret-token
  Content-Type: application/json

Body: (see sample_request.json)
```

### Generate Proforma Invoice

```bash
POST /generate-proforma-invoice
Headers: 
  Authorization: Bearer your-secret-token
  Content-Type: application/json

Body: (see sample_proforma_request.json)
```

For detailed proforma invoice documentation, see [PROFORMA_INVOICE_USAGE.md](PROFORMA_INVOICE_USAGE.md)

## 📝 JSON Request Structure

```json
{
  "invoice": {
    "number": "00TI25-00000011",
    "date_of_issuing": "March 6, 2025",
    "date_of_supply": "March 6, 2025"
  },
  "issued_to": {
    "name": "Customer Name",
    "address": "Address Line 1<br/>City State Zip",
    "trn": "Tax Registration Number (optional)",
    "tel": "Phone (optional)",
    "email": "customer@example.com"
  },
  "terms": {
    "payment_terms": "Payment on Delivery",
    "delivery_terms": "Ex-works Dubai"
  },
  "items": [
    {
      "description": "Item description",
      "quantity": 1.0,
      "uom": "Pcs",
      "price_aed": 1000.00,
      "discount_pct": 10.0,
      "vat_pct": 5,
      "rate_usd": 3.6725
    }
  ],
  "supply_total_text": "One thousand AED ONLY",
  "recipient_emails": [
    "customer@example.com",
    "accounting@yourcompany.com"
  ]
}
```

## 🧪 Testing with cURL

### Test Token

```bash
curl -X POST http://localhost:8000/test-token \
  -H "Authorization: Bearer your-secret-token"
```

### Generate Invoice

```bash
curl -X POST http://localhost:8000/generate-invoice \
  -H "Authorization: Bearer your-secret-token" \
  -H "Content-Type: application/json" \
  -d @invoice_data.json
```

### Using Python

```python
import requests

url = "https://your-hetzner-server.com/generate-invoice"
headers = {
    "Authorization": "Bearer your-secret-token",
    "Content-Type": "application/json"
}

data = {
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

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 🔒 Security

- **Token Authentication**: All endpoints (except `/` and `/health`) require valid token
- **Environment Variables**: Secrets stored in environment, not code
- **HTTPS**: Always use HTTPS in production

### Generating a Strong Token

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚢 Deployment to Hetzner

### 1. Setup Server

```bash
# Install Python and dependencies
apt update
apt install python3 python3-pip python3-venv nginx

# Create app directory
mkdir -p /var/www/invoice-api
cd /var/www/invoice-api

# Copy files
# (upload via scp, git, etc.)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create systemd Service

Create `/etc/systemd/system/invoice-api.service`:

```ini
[Unit]
Description=Invoice Generator API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/invoice-api
Environment="PATH=/var/www/invoice-api/venv/bin"
EnvironmentFile=/var/www/invoice-api/.env
ExecStart=/var/www/invoice-api/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

### 3. Configure Nginx

Create `/etc/nginx/sites-available/invoice-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/invoice-api /etc/nginx/sites-enabled/
systemctl restart nginx
```

### 4. Setup SSL with Certbot

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

### 5. Start Service

```bash
systemctl start invoice-api
systemctl enable invoice-api
systemctl status invoice-api
```

## 📊 Monitoring

```bash
# View logs
journalctl -u invoice-api -f

# Check status
systemctl status invoice-api

# Restart service
systemctl restart invoice-api
```

## 🔧 Troubleshooting

### "RESEND_API_KEY not configured"
- Make sure `.env` file exists with `RESEND_API_KEY`
- Export environment variables before running

### "Invalid API token"
- Check `Authorization` header format: `Bearer your-token`
- Verify `API_SECRET_TOKEN` in `.env` matches your request

### WeasyPrint errors
- Install system dependencies:
  ```bash
  apt install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
  ```

## 📧 Resend Configuration

1. Sign up at [resend.com](https://resend.com)
2. Verify your sending domain
3. Create API key
4. Add to `.env` file

## 💡 Tips

- Use strong, random tokens (32+ characters)
- Keep `.env` file secure (never commit to git)
- Monitor logs for failed requests
- Use HTTPS in production
- Rate limit in production (use nginx or fastapi middleware)
- Send invoice copy to your own email for records

---

**Ready to deploy!** 🚀


# Quick Start Guide

Get your invoice API running in 5 minutes!

## 🚀 Local Development

### 1. Setup Environment

```bash
cd fast_api_invoice_server

# Copy environment template
cp .env.example .env

# Edit with your values
nano .env
```

Add to `.env`:
```env
API_SECRET_TOKEN=my-super-secret-token-12345
RESEND_API_KEY=re_your_api_key_here
FROM_EMAIL=invoices@yourdomain.com
```

### 2. Start Server

```bash
./start.sh
```

Server will start at `http://localhost:8000`

### 3. Test It

Open another terminal:

```bash
# Set your token
export API_SECRET_TOKEN=my-super-secret-token-12345

# Run tests
./test_api.py
```

## 📤 Send Test Invoice

### Using cURL

```bash
curl -X POST http://localhost:8000/generate-invoice \
  -H "Authorization: Bearer my-super-secret-token-12345" \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-invoice",
    headers={"Authorization": "Bearer my-super-secret-token-12345"},
    json={
        "invoice": {
            "number": "TEST-001",
            "date_of_issuing": "March 6, 2025",
            "date_of_supply": "March 6, 2025"
        },
        "issued_to": {
            "name": "Test Customer",
            "address": "123 Test St",
            "email": "customer@example.com"
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
    }
)

print(response.json())
```

## 🌐 Deploy to Hetzner

### 1. Prepare Server

```bash
# SSH into your Hetzner server
ssh root@your-server-ip

# Install dependencies
apt update
apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx
apt install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev

# Create app directory
mkdir -p /var/www/invoice-api
cd /var/www/invoice-api
```

### 2. Upload Files

From your local machine:

```bash
# Upload entire directory
scp -r fast_api_invoice_server root@your-server-ip:/var/www/invoice-api/

# Or clone from git
# ssh into server, then:
git clone your-repo.git /var/www/invoice-api
```

### 3. Setup on Server

```bash
cd /var/www/invoice-api/fast_api_invoice_server

# Create virtual environment
python3 -m venv /var/www/invoice-api/venv
source /var/www/invoice-api/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Add your production values (API_SECRET_TOKEN, RESEND_API_KEY, FROM_EMAIL)

# Set permissions
chown -R www-data:www-data /var/www/invoice-api
chmod 600 .env
```

### 4. Install systemd Service

```bash
# Copy service file
cp invoice-api.service /etc/systemd/system/

# Update paths in service file if needed
nano /etc/systemd/system/invoice-api.service

# Reload systemd
systemctl daemon-reload

# Start service
systemctl start invoice-api
systemctl enable invoice-api

# Check status
systemctl status invoice-api
```

### 5. Setup Nginx

```bash
# Create nginx config
nano /etc/nginx/sites-available/invoice-api
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}
```

```bash
# Enable site
ln -s /etc/nginx/sites-available/invoice-api /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 6. Setup SSL (HTTPS)

```bash
certbot --nginx -d your-domain.com
```

### 7. Test It

```bash
curl -X POST https://your-domain.com/test-token \
  -H "Authorization: Bearer your-secret-token"
```

## 🔥 Production Checklist

- [ ] Strong API token (32+ characters)
- [ ] Valid Resend API key
- [ ] Domain configured with DNS
- [ ] SSL certificate installed
- [ ] `.env` file secured (chmod 600)
- [ ] Service running and enabled
- [ ] Nginx configured and running
- [ ] Firewall configured (allow 80, 443)
- [ ] Test endpoint working
- [ ] Test invoice generation
- [ ] Email delivery working
- [ ] Monitoring/logs setup

## 🛠️ Useful Commands

```bash
# View logs
journalctl -u invoice-api -f

# Restart service
systemctl restart invoice-api

# Check if running
systemctl status invoice-api

# Test locally on server
curl http://localhost:8000/health

# Update code
cd /var/www/invoice-api
git pull
systemctl restart invoice-api
```

## ❓ Troubleshooting

**Service won't start:**
```bash
# Check logs
journalctl -u invoice-api -n 50

# Check permissions
ls -la /var/www/invoice-api

# Test manually
cd /var/www/invoice-api/fast_api_invoice_server
source /var/www/invoice-api/venv/bin/activate
python main.py
```

**Email not sending:**
- Verify Resend API key in `.env`
- Check domain is verified in Resend
- Check logs for error messages

**401 Unauthorized:**
- Check Authorization header format
- Verify API_SECRET_TOKEN matches

---

**Need help?** Check the full README.md


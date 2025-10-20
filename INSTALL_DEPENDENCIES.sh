#!/bin/bash
# Install system dependencies for WeasyPrint on Ubuntu/Debian

echo "📦 Installing WeasyPrint system dependencies..."
echo ""

# Update package list
apt-get update

# Install required system libraries
apt-get install -y \
  libpango-1.0-0 \
  libpangoft2-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libffi-dev \
  shared-mime-info

echo ""
echo "✅ System dependencies installed successfully!"
echo ""
echo "Now restart your FastAPI server:"
echo "  cd /var/invoice/invoices_sc"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"


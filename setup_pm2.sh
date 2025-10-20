#!/bin/bash
# Setup Invoice API with PM2

echo "🚀 Setting up Invoice API with PM2..."
echo ""

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "📦 Installing PM2..."
    npm install -g pm2
else
    echo "✅ PM2 is already installed"
fi

echo ""
echo "📁 Creating logs directory..."
mkdir -p /var/invoice/invoices_sc/logs

echo ""
echo "🔧 Starting Invoice API with PM2..."
cd /var/invoice/invoices_sc
pm2 start ecosystem.config.js

echo ""
echo "💾 Saving PM2 configuration..."
pm2 save

echo ""
echo "🔄 Setting up PM2 to start on boot..."
pm2 startup

echo ""
echo "✅ Invoice API is now running with PM2!"
echo ""
echo "📊 PM2 Status:"
pm2 status

echo ""
echo "📝 Useful PM2 Commands:"
echo "  • View status:     pm2 status"
echo "  • View logs:       pm2 logs invoice-api"
echo "  • Stop server:     pm2 stop invoice-api"
echo "  • Restart server:  pm2 restart invoice-api"
echo "  • Monitor:         pm2 monit"
echo "  • Delete from PM2: pm2 delete invoice-api"
echo ""


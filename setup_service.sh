#!/bin/bash
# Setup Invoice API as a systemd service

echo "🚀 Setting up Invoice API as a background service..."
echo ""

# Copy service file to systemd directory
echo "1️⃣ Installing systemd service..."
cp invoice-api-production.service /etc/systemd/system/invoice-api.service

# Reload systemd
echo "2️⃣ Reloading systemd daemon..."
systemctl daemon-reload

# Enable service to start on boot
echo "3️⃣ Enabling service to start on boot..."
systemctl enable invoice-api

# Start the service
echo "4️⃣ Starting the service..."
systemctl start invoice-api

# Show status
echo ""
echo "✅ Service installed and started!"
echo ""
echo "📊 Service Status:"
systemctl status invoice-api --no-pager

echo ""
echo "📝 Useful Commands:"
echo "  • Check status:    systemctl status invoice-api"
echo "  • Stop service:    systemctl stop invoice-api"
echo "  • Start service:   systemctl start invoice-api"
echo "  • Restart service: systemctl restart invoice-api"
echo "  • View logs:       journalctl -u invoice-api -f"
echo ""


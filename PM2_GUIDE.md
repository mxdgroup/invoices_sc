# PM2 Setup Guide for Invoice API

## 🚀 Quick Setup

### 1. Install PM2 (if not installed)
```bash
npm install -g pm2
```

### 2. Start the Invoice API
```bash
cd /var/invoice/invoices_sc

# Option A: Using ecosystem file (recommended)
pm2 start ecosystem.config.js

# Option B: Direct command
pm2 start "venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000" --name invoice-api
```

### 3. Save and Auto-start on Boot
```bash
pm2 save
pm2 startup
# Follow the command it shows (will create startup script)
```

---

## 📋 Common Commands

### Status & Monitoring
```bash
pm2 status              # Show all processes
pm2 list                # Same as status
pm2 info invoice-api    # Detailed info
pm2 monit               # Real-time monitoring dashboard
```

### Logs
```bash
pm2 logs invoice-api           # View logs (live)
pm2 logs invoice-api --lines 100  # Last 100 lines
pm2 logs --err                 # Only errors
pm2 flush                      # Clear all logs
```

### Control
```bash
pm2 start invoice-api          # Start
pm2 stop invoice-api           # Stop
pm2 restart invoice-api        # Restart
pm2 reload invoice-api         # Reload (0-downtime)
pm2 delete invoice-api         # Remove from PM2
```

### Advanced
```bash
pm2 scale invoice-api 4        # Scale to 4 instances
pm2 restart invoice-api --update-env  # Restart with new env vars
pm2 reset invoice-api          # Reset restart counter
```

---

## 🔧 Configuration

Your PM2 configuration is in `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [{
    name: 'invoice-api',
    script: 'venv/bin/uvicorn',
    args: 'main:app --host 0.0.0.0 --port 8000',
    cwd: '/var/invoice/invoices_sc',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
```

### Modify Settings
```bash
# Edit the file
nano ecosystem.config.js

# Reload with new config
pm2 reload ecosystem.config.js
```

---

## 📊 Monitoring

### Real-time Dashboard
```bash
pm2 monit
```

### Web Dashboard (Optional)
```bash
pm2 web
# Access at: http://your-server:9615
```

### PM2 Plus (Cloud Monitoring - Optional)
```bash
pm2 plus
# Follow the prompts to link your server
```

---

## 🔄 Auto-restart on Reboot

### Setup
```bash
pm2 startup
# Copy and run the command it shows

pm2 save
# This saves the current process list
```

### Test
```bash
# Reboot your server
reboot

# After reboot, check if it's running
pm2 status
```

### Disable auto-start
```bash
pm2 unstartup
```

---

## 📁 Log Files

By default, logs are stored in:
- Error logs: `/var/invoice/invoices_sc/logs/error.log`
- Output logs: `/var/invoice/invoices_sc/logs/out.log`
- Combined: `/var/invoice/invoices_sc/logs/combined.log`

### Manage Logs
```bash
pm2 logs invoice-api           # View live logs
pm2 logs invoice-api --lines 200  # Last 200 lines
pm2 flush                      # Clear all logs
```

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check detailed error
pm2 logs invoice-api --err

# Delete and recreate
pm2 delete invoice-api
pm2 start ecosystem.config.js
```

### Check if port is in use
```bash
lsof -i :8000
# or
netstat -tuln | grep 8000
```

### Restart with fresh state
```bash
pm2 delete invoice-api
pm2 flush
pm2 start ecosystem.config.js
```

---

## 📈 Performance Tips

### Use Cluster Mode (Multiple Workers)
Edit `ecosystem.config.js`:
```javascript
instances: 4,  // or 'max' for all CPU cores
exec_mode: 'cluster'
```

### Memory Limits
```javascript
max_memory_restart: '1G'  // Restart if exceeds 1GB
```

### Watch for Changes (Development)
```javascript
watch: true,
ignore_watch: ['node_modules', 'logs', '*.log']
```

---

## ✅ Quick Reference Card

| Action | Command |
|--------|---------|
| Start | `pm2 start ecosystem.config.js` |
| Stop | `pm2 stop invoice-api` |
| Restart | `pm2 restart invoice-api` |
| Status | `pm2 status` |
| Logs | `pm2 logs invoice-api` |
| Monitor | `pm2 monit` |
| Delete | `pm2 delete invoice-api` |
| Save | `pm2 save` |
| Auto-start | `pm2 startup` + `pm2 save` |

---

## 🆚 PM2 vs Systemd

| Feature | PM2 | Systemd |
|---------|-----|---------|
| Easy to use | ✅ Very easy | ⚠️ More complex |
| Cross-platform | ✅ Yes | ❌ Linux only |
| Real-time logs | ✅ `pm2 logs` | ⚠️ `journalctl` |
| Monitoring | ✅ `pm2 monit` | ❌ Need external tools |
| Cluster mode | ✅ Built-in | ❌ Manual setup |
| Node.js required | ❌ Yes | ✅ No |

**Recommendation**: PM2 is easier and better for most use cases! ✨

---

## 🎯 Example Workflow

```bash
# 1. First time setup
cd /var/invoice/invoices_sc
pm2 start ecosystem.config.js
pm2 save
pm2 startup  # Follow the command shown

# 2. Deploy updates
git pull  # or copy new files
pm2 restart invoice-api

# 3. Check if running
pm2 status

# 4. View logs if issues
pm2 logs invoice-api

# 5. That's it! ✅
```

---

**Documentation**: https://pm2.keymetrics.io/docs/usage/quick-start/


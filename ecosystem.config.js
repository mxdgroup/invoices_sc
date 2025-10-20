module.exports = {
  apps: [{
    name: 'invoice-api',
    script: 'venv/bin/uvicorn',
    args: 'main:app --host 0.0.0.0 --port 8000',
    cwd: '/var/invoice/invoices_sc',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: '/var/invoice/invoices_sc/logs/error.log',
    out_file: '/var/invoice/invoices_sc/logs/out.log',
    log_file: '/var/invoice/invoices_sc/logs/combined.log',
    time: true
  }]
};


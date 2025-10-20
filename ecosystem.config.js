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
      NODE_ENV: 'production',
      API_SECRET_TOKEN: 'your-super-secret-token-here-change-this',
      RESEND_API_KEY: 're_N6grtNCm_8P7xKShtr2aWuQ7hjuMfNYkS',
      FROM_EMAIL: 'invoices@invoices.suzannecode.com',
      TEST_EMAIL: 'ivan.f@mxd.digital'
    },
    error_file: '/var/invoice/invoices_sc/logs/error.log',
    out_file: '/var/invoice/invoices_sc/logs/out.log',
    log_file: '/var/invoice/invoices_sc/logs/combined.log',
    time: true
  }]
};


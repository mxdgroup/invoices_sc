#!/usr/bin/env python3
"""
Generate invoice HTML from JSON data
"""
import json
import os

def format_number(n, decimals=2):
    """Format number with thousands separator"""
    return f"{n:,.{decimals}f}"

def calculate_item_totals(items):
    """Calculate all totals from items"""
    total_discount = 0
    sub_total = 0
    total_vat = 0
    total_aed = 0
    total_usd = 0
    
    rows_html = []
    
    for idx, item in enumerate(items, 1):
        qty = item['quantity']
        price = item['price_aed']
        discount_pct = item.get('discount_pct', 0)
        vat_pct = item.get('vat_pct', 0)
        rate_usd = item.get('rate_usd', 0)
        
        # Calculations
        gross = price * qty
        discount_amt = gross * (discount_pct / 100)
        amount_excl = gross - discount_amt
        vat_amt = amount_excl * (vat_pct / 100)
        amount_incl = amount_excl + vat_amt
        amount_usd = amount_incl / rate_usd if rate_usd else 0
        
        # Accumulate totals
        total_discount += discount_amt
        sub_total += amount_excl
        total_vat += vat_amt
        total_aed += amount_incl
        total_usd += amount_usd
        
        # Generate row HTML
        row = f"""        <tr>
          <td class="center">{idx}</td>
          <td>{item['description']}</td>
          <td class="center">{format_number(qty, 3)}</td>
          <td class="center">{item['uom']}</td>
          <td class="right">{format_number(price, 2)}</td>
          <td class="right">{format_number(discount_pct, 2)}</td>
          <td class="right">{format_number(amount_excl, 2)}</td>
          <td class="center">{format_number(vat_pct, 0)}</td>
          <td class="right">{format_number(vat_amt, 2)}</td>
          <td class="right">{format_number(amount_incl, 2)}</td>
          <td class="right">{format_number(rate_usd, 6)}</td>
          <td class="right">{format_number(amount_usd, 2)}</td>
        </tr>"""
        rows_html.append(row)
    
    return {
        'rows': '\n'.join(rows_html),
        'total_discount': format_number(total_discount, 2),
        'sub_total': format_number(sub_total, 2),
        'total_vat': format_number(total_vat, 2),
        'total_aed': format_number(total_aed, 2),
        'total_usd': format_number(total_usd, 2)
    }

def generate_html(json_file, output_html):
    """Generate HTML invoice from JSON data"""
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Hardcoded company information
    issued_by = {
        'company_name': 'SUZANNE CODE JEWELLERY TRADING L.L.C.',
        'address': 'Shop B5-OF-05 ,Burj Khalifa, Emaar The Dubai Mall Fountain Views, PO Box:9440, Dubai, UAE',
        'trn': '104644174200003',
        'tel': '+971505572796',
        'email': 'sue@suzannecode.com'
    }
    
    bank_details = {
        'bank_name': 'Abu Dhabi Islamic Bank',
        'iban': 'AE080500000000019283818',
        'swift': 'ABDIAEADXXX',
        'beneficiary': 'SUZANNE CODE JEWELLERY TRADING L.L.C.'
    }
    
    logo = {
        'text': 'SUZANNE CODE',
        'svg_data': "data:image/svg+xml;utf8,<?xml version='1.0' encoding='UTF-8'?><svg xmlns='http://www.w3.org/2000/svg' width='120' height='42' viewBox='0 0 120 42'><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='10' fill='%23000'>SUZANNE CODE</text></svg>"
    }
    
    # Calculate totals
    totals = calculate_item_totals(data['items'])
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>TAX INVOICE</title>
  <style>
    /* --- Reset & base --- */
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: #000;
      background: #fff;
    }}

    /* --- Page sizing for print --- */
    @page {{ size: 370mm 290mm; margin: 10mm; }}
    @media print {{
      body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
      .page {{ box-shadow: none; margin: 0; }}
    }}

    /* --- Page canvas --- */
    .page {{
      width: 350mm; /* Wider invoice layout */
      min-height: 185mm;
      margin: 10mm auto;
      padding: 6mm 8mm;
      background: #fff;
      box-shadow: 0 0 0.5mm rgba(0,0,0,.15);
      border: 1px solid #dcdcdc;
    }}

    /* --- Header --- */
    .header {{ display: grid; grid-template-columns: 1fr auto; align-items: start; }}
    .title {{ font-size: 20pt; font-weight: 700; letter-spacing: 0.3pt; }}
    .logo {{ height: 42px; opacity: 0.9; }}

    .meta {{ margin-top: 4px; font-size: 10.5pt; line-height: 1.4; }}
    .meta strong {{ font-weight: 700; }}

    /* --- Box sections --- */
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 10px; }}
    .box {{ border: 1px solid #9ea3a8; }}
    .box .box-title {{ background: #e9edf2; border-bottom: 1px solid #9ea3a8; padding: 6px 8px; font-weight: 700; font-size: 10pt; }}
    .box .box-body {{ padding: 8px; font-size: 10pt; line-height: 1.45; }}
    .label {{ width: 82px; display: inline-block; font-weight: 700; }}

    .box-slim {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }}

    /* --- Items table --- */
    .items {{ margin-top: 10px; border: 1px solid #9ea3a8; border-collapse: separate; border-spacing: 0; width: 100%; font-size: 10pt; }}
    .items th, .items td {{ border-right: 1px solid #9ea3a8; border-bottom: 1px solid #9ea3a8; padding: 6px; vertical-align: top; }}
    .items th:last-child, .items td:last-child {{ border-right: 0; }}
    .items thead th {{ background: #e9edf2; font-weight: 700; text-align: center; }}
    .items tbody td {{ background: #fff; }}
    .items .center {{ text-align: center; }}
    .items .right {{ text-align: right; white-space: nowrap; }}

    .supply-total {{ border: 1px solid #9ea3a8; border-top: 0; padding: 6px; font-size: 10pt; }}
    .supply-total .label-wide {{ font-weight: 700; }}

    /* --- Totals panel --- */
    .totals-row {{ display: grid; grid-template-columns: 1.4fr 1fr; gap: 8px; margin-top: 6px; }}
    .totals {{ margin-left: auto; width: 100%; border: 1px solid #9ea3a8; border-collapse: separate; border-spacing: 0; font-size: 10pt; }}
    .totals td {{ padding: 6px; border-bottom: 1px solid #9ea3a8; }}
    .totals tr:last-child td {{ border-bottom: 0; }}
    .totals td:first-child {{ background: #e9edf2; font-weight: 700; width: 55%; }}
    .totals td:last-child {{ text-align: right; white-space: nowrap; }}

    /* --- Footer --- */
    .footer {{ margin-top: 18mm; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; align-items: end; }}
    .sign-block {{ min-height: 28mm; border-top: 1px solid #9ea3a8; padding-top: 4mm; position: relative; }}
    .sign-title {{ position: absolute; top: -11mm; font-weight: 700; font-size: 10pt; }}
    .stamp {{
      position: absolute; left: 28mm; top: -10mm; width: 38mm; height: 38mm; border-radius: 50%; border: 2px solid #1a6fb4; opacity: .25;
    }}

    /* Utility */
    .muted {{ color: #444; }}
    .nowrap {{ white-space: nowrap; }}
    .w-20 {{ width: 20mm; }}
  </style>
</head>
<body>
  <div class="page">
    <!-- Header -->
    <div class="header">
      <div>
        <div class="title">TAX INVOICE</div>
        <div class="meta">
          <div><strong># {data['invoice']['number']}</strong></div>
          <div><strong>Date of Issuing:</strong> {data['invoice']['date_of_issuing']}</div>
          <div><strong>Date of Supply:</strong> {data['invoice']['date_of_supply']}</div>
        </div>
      </div>
      <img class="logo" src="{logo['svg_data']}" alt="Logo" />
    </div>

    <!-- Issued By / Issued To -->
    <div class="grid-2">
      <div class="box">
        <div class="box-title">Issued By:</div>
        <div class="box-body">
          <div><strong>{issued_by['company_name']}</strong></div>
          <div><span class="label">Address:</span> {issued_by['address']}</div>
          <div><span class="label">TRN:</span> {issued_by['trn']}</div>
          <div><span class="label">Tel.:</span> {issued_by['tel']}</div>
          <div><span class="label">E-mail:</span> {issued_by['email']}</div>
        </div>
      </div>
      <div class="box">
        <div class="box-title">Issued To:</div>
        <div class="box-body">
          <div><strong>{data['issued_to']['name']}</strong></div>
          <div><span class="label">Address:</span> {data['issued_to']['address']}</div>
          <div><span class="label">TRN:</span> {data['issued_to']['trn']}</div>
          <div><span class="label">Tel.:</span> {data['issued_to']['tel']}</div>
          <div><span class="label">E-mail:</span> {data['issued_to']['email']}</div>
        </div>
      </div>
    </div>

    <!-- Bank details / Payment terms -->
    <div class="box-slim">
      <div class="box">
        <div class="box-title">Bank Details:</div>
        <div class="box-body">
          <div><strong>{bank_details['bank_name']}</strong></div>
          <div><span class="label">IBAN:</span> {bank_details['iban']}</div>
          <div><span class="label">SWIFT:</span> {bank_details['swift']}</div>
          <div><span class="label">Beneficiary:</span> {bank_details['beneficiary']}</div>
        </div>
      </div>
      <div class="box">
        <div class="box-title">Payment and Delivery Terms:</div>
        <div class="box-body">
          <div><strong>Payment Terms:</strong> {data['terms']['payment_terms']}</div>
          <div style="margin-top:4px;"><strong>Delivery Terms:</strong> {data['terms']['delivery_terms']}</div>
        </div>
      </div>
    </div>

    <!-- Items table -->
    <table class="items">
      <thead>
        <tr>
          <th class="w-20">#</th>
          <th>Description</th>
          <th>Quantity</th>
          <th>UOM</th>
          <th>Price<br/>(Excl. VAT),<br/>AED</th>
          <th>Discount,<br/>%</th>
          <th>Amount<br/>(Excl. VAT),<br/>AED</th>
          <th>VAT,<br/>%</th>
          <th>VAT<br/>Amount,<br/>AED</th>
          <th>Amount<br/>(Incl. VAT),<br/>AED</th>
          <th>Rate,<br/>USD</th>
          <th>Amount<br/>(Incl. VAT),<br/>USD</th>
        </tr>
      </thead>
      <tbody>
{totals['rows']}
      </tbody>
    </table>

    <div class="supply-total"><span class="label-wide">TOTAL OF SUPPLY:</span> {data['supply_total_text']}</div>

    <!-- Totals -->
    <div class="totals-row">
      <div></div>
      <table class="totals">
        <tr><td>Total Discount, AED:</td><td>{totals['total_discount']}</td></tr>
        <tr><td>Sub Total, AED:</td><td>{totals['sub_total']}</td></tr>
        <tr><td>Total VAT, AED:</td><td>{totals['total_vat']}</td></tr>
        <tr><td>Total, AED:</td><td>{totals['total_aed']}</td></tr>
        <tr><td>Total, USD:</td><td>{totals['total_usd']}</td></tr>
      </table>
    </div>

    <!-- Footer signatures -->
    <div class="footer">
      <div class="sign-block">
        <div class="sign-title">Released By</div>
        <div class="stamp" aria-hidden="true"></div>
      </div>
      <div class="sign-block">
        <div class="sign-title">Received By</div>
      </div>
    </div>
  </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated HTML: {output_html}")
    return output_html

if __name__ == "__main__":
    generate_html("invoice_data.json", "invoice_static.html")


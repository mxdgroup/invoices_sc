#!/usr/bin/env python3
"""
Convert HTML invoice to PDF using WeasyPrint
"""
from weasyprint import HTML, CSS
import os
import re

def html_to_pdf(html_file, output_pdf=None, base_height=377, item_height=30):
    """
    Convert HTML file to PDF with dynamic height based on item count
    
    Args:
        html_file: Path to the HTML file
        output_pdf: Path to output PDF (optional, defaults to same name as HTML)
        base_height: Base page height in mm (default: 377mm)
        item_height: Additional height per item in mm (default: 30mm)
    """
    if not os.path.exists(html_file):
        print(f"Error: File '{html_file}' not found")
        return False
    
    # Generate output filename if not provided
    if output_pdf is None:
        base_name = os.path.splitext(html_file)[0]
        output_pdf = f"{base_name}.pdf"
    
    try:
        # Count items in the HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count actual product rows in tbody (excluding "Amount in Words" row)
            tbody_match = re.search(r'<tbody>(.*?)</tbody>', content, re.DOTALL)
            if tbody_match:
                tbody_content = tbody_match.group(1)
                # Count all tr elements
                all_rows = len(re.findall(r'<tr>', tbody_content))
                # Subtract 1 for the "Amount in Words" row
                item_count = max(1, all_rows - 1)
            else:
                item_count = 1
        
        # Calculate dynamic height
        page_height = base_height + (item_count * item_height)
        
        print(f"Converting '{html_file}' to PDF...")
        print(f"  Items found: {item_count}")
        print(f"  Calculated page height: {page_height}mm (base: {base_height}mm + {item_count} items × {item_height}mm)")
        
        # Convert HTML to PDF with custom CSS to handle page size
        css_string = f'''
            @page {{
                size: 400mm {page_height}mm;
                margin: 12mm;
            }}
        '''
        
        HTML(filename=html_file).write_pdf(
            output_pdf,
            stylesheets=[CSS(string=css_string)]
        )
        
        print(f"✓ Successfully created: {output_pdf}")
        print(f"  File size: {os.path.getsize(output_pdf) / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"✗ Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        raise  # Re-raise the exception so calling code can handle it

if __name__ == "__main__":
    # Convert static HTML to PDF
    html_to_pdf("invoice_static.html", "invoice.pdf")


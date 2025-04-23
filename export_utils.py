import pandas as pd
import base64
from io import BytesIO
import datetime
from weasyprint import HTML

def generate_excel(line_items, questionnaire, production_vars, low_quote, high_quote, recommended):
    """Generate an Excel file with quote details"""
    buffer = BytesIO()
    
    # Create a Pandas Excel writer using BytesIO as the file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Convert line items to DataFrame
        df = pd.DataFrame(line_items).T.reset_index()
        df.columns = ["Item", "Low (Rp)", "High (Rp)"]
        
        # Write line items to a sheet
        df.to_excel(writer, sheet_name='Quote Breakdown', index=False)
        
        # Create summary sheet
        summary_data = {
            'Item': ['Low Estimate', 'Recommended Price', 'High Estimate'],
            'Amount (Rp)': [low_quote, recommended, high_quote]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Quote Summary', index=False)
        
        # Create project details sheet
        project_details = []
        
        # Add questionnaire details
        for key, value in questionnaire.items():
            if key == 'distribution' and isinstance(value, list):
                value = ', '.join(value)
            elif key == 'special_requirements' and isinstance(value, list):
                value = ', '.join(value)
            elif key in ['shoot_date', 'delivery_date'] and value is not None:
                value = value.strftime('%Y-%m-%d')
                
            project_details.append({
                'Category': 'Client Brief',
                'Item': key.replace('_', ' ').title(),
                'Value': value
            })
            
        # Add production variables
        for key, value in production_vars.items():
            project_details.append({
                'Category': 'Production Variables',
                'Item': key.replace('_', ' ').title(),
                'Value': value
            })
            
        # Create DataFrame and write to Excel
        details_df = pd.DataFrame(project_details)
        details_df.to_excel(writer, sheet_name='Project Details', index=False)
        
    # Get the Excel data
    buffer.seek(0)
    return buffer.getvalue()

def get_table_download_link(line_items, questionnaire, production_vars, low_quote, high_quote, recommended):
    """Generate a link to download the Excel file"""
    excel_data = generate_excel(line_items, questionnaire, production_vars, low_quote, high_quote, recommended)
    b64 = base64.b64encode(excel_data).decode()
    
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"lapis_quote_{current_date}.xlsx"
    
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel Quote</a>'
    return href

def generate_pdf_html(line_items, questionnaire, production_vars, low_quote, high_quote, recommended):
    """Generate HTML for PDF export (placeholder)"""
    # In a real implementation, you would use a PDF library like reportlab or WeasyPrint
    # For this scaffold, we'll just return HTML that could be converted to PDF
    
    # Format currency values
    low_quote_fmt = f"Rp {low_quote:,.0f}".replace(",", ".")
    high_quote_fmt = f"Rp {high_quote:,.0f}".replace(",", ".")
    recommended_fmt = f"Rp {recommended:,.0f}".replace(",", ".")
    
    # Create HTML content
    html = f"""
    <html>
    <head>
        <title>Lapis Visuals - Project Quote</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2C3E50; }}
            .summary {{ display: flex; justify-content: space-between; margin: 20px 0; }}
            .summary-item {{ 
                padding: 15px; 
                background-color: #f8f9fa; 
                border-radius: 5px;
                width: 30%;
                text-align: center;
            }}
            .summary-value {{ 
                font-size: 24px; 
                font-weight: bold;
                margin: 10px 0;
            }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <h1>Lapis Visuals - Project Quote</h1>
        <p>Date: {datetime.datetime.now().strftime('%Y-%m-%d')}</p>
        
        <h2>Quote Summary</h2>
        <div class="summary">
            <div class="summary-item">
                <div>Low Estimate</div>
                <div class="summary-value">{low_quote_fmt}</div>
            </div>
            <div class="summary-item">
                <div>Recommended</div>
                <div class="summary-value">{recommended_fmt}</div>
            </div>
            <div class="summary-item">
                <div>High Estimate</div>
                <div class="summary-value">{high_quote_fmt}</div>
            </div>
        </div>
        
        <h2>Project Details</h2>
        <table>
            <tr>
                <th>Item</th>
                <th>Value</th>
            </tr>
    """
    
    # Add questionnaire details
    for key, value in questionnaire.items():
        if key in ['distribution', 'special_requirements'] and isinstance(value, list):
            value = ', '.join(value) if value else 'None'
        elif key in ['shoot_date', 'delivery_date'] and value is not None:
            value = value.strftime('%Y-%m-%d')
        elif value is None or (isinstance(value, list) and not value):
            value = 'None'
            
        html += f"""
        <tr>
            <td>{key.replace('_', ' ').title()}</td>
            <td>{value}</td>
        </tr>
        """
    
    # Add line items breakdown
    html += """
        </table>
        
        <h2>Cost Breakdown</h2>
        <table>
            <tr>
                <th>Item</th>
                <th>Low (Rp)</th>
                <th>High (Rp)</th>
            </tr>
    """
    
    # Add line items
    for item, values in line_items.items():
        low = f"Rp {values['low']:,.0f}".replace(",", ".")
        high = f"Rp {values['high']:,.0f}".replace(",", ".")
        
        html += f"""
        <tr>
            <td>{item}</td>
            <td>{low}</td>
            <td>{high}</td>
        </tr>
        """
    
    # Finish HTML
    html += """
        </table>
        
        <div class="footer">
            <p>Generated by Lapis Visuals Pricing Calculator</p>
            <p>This quote is valid for 30 days from the date above.</p>
        </div>
    </body>
    </html>
    """
    
    return html 

def generate_pdf_bytes(line_items, questionnaire, production_vars, low_quote, high_quote, recommended):
    """Generate PDF bytes from HTML using WeasyPrint"""
    html_content = generate_pdf_html(line_items, questionnaire, production_vars, low_quote, high_quote, recommended)
    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes

def get_pdf_download_button(line_items, questionnaire, production_vars, low_quote, high_quote, recommended):
    """Return a Streamlit download button for the PDF file"""
    import streamlit as st
    import datetime
    pdf_bytes = generate_pdf_bytes(line_items, questionnaire, production_vars, low_quote, high_quote, recommended)
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"lapis_quote_{current_date}.pdf"
    return st.download_button(
        label="Download PDF Quote",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf"
    ) 
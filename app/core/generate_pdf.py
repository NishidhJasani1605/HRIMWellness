import os
import markdown
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from datetime import datetime
import tempfile

def markdown_to_html(markdown_content, user_data):
    """Convert markdown content to HTML with proper styling"""
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'nl2br'])
    
    # Get user information for the header
    user_name = user_data.get('Full Name', 'Client')
    user_email = user_data.get('Email', '')
    user_phone = user_data.get('WhatsApp Contact Number', '')
    date_generated = datetime.now().strftime("%d %B, %Y")
    
    # Basic styles
    styles = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }
        
        .header {
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #007ACC;
            margin-bottom: 20px;
        }
        
        .header h1 {
            color: #007ACC;
            margin: 0;
            font-size: 24px;
        }
        
        .header .sanskrit {
            font-style: italic;
            color: #555;
            margin: 5px 0;
        }
        
        .header .contact {
            font-size: 12px;
            color: #555;
            margin-top: 10px;
        }
        
        .client-info {
            margin: 20px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        
        .content {
            margin: 20px;
        }
        
        h1, h2, h3 {
            color: #007ACC;
        }
        
        h2 {
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            margin-top: 20px;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        
        table, th, td {
            border: 1px solid #ddd;
        }
        
        th, td {
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
        }
        
        ul, ol {
            margin-left: 20px;
        }
        
        .footer {
            text-align: center;
            font-size: 10px;
            color: #777;
            margin-top: 30px;
            border-top: 1px solid #ddd;
            padding-top: 10px;
        }
        
        @page {
            size: A4;
            margin: 2cm;
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
            }
        }
    </style>
    """
    
    # Create HTML document with header and footer
    complete_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Wellness Plan - {user_name}</title>
        {styles}
    </head>
    <body>
        <div class="header">
            <h1>HRIM Wellness Centre</h1>
            <div class="sanskrit">॥स्वस्थस्य स्वास्थ्य रक्षणम॥</div>
            <div>503, Takshshila Apartment, Dayalaji Ashram Marg, Majura Gate, Surat – 395001</div>
            <div class="contact">📞 +91 94279 81235 | 📧 hrimwellness@gmail.com | 🌐 www.hrimwellness.in</div>
        </div>
        
        <div class="client-info">
            <strong>Client:</strong> {user_name}<br>
            <strong>Date Generated:</strong> {date_generated}<br>
            <strong>Email:</strong> {user_email}<br>
            <strong>Phone:</strong> {user_phone}
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="footer">
            This wellness plan is personalized based on the information provided. 
            Please consult your healthcare provider before starting any new diet or exercise regimen.
            <br>© HRIM Wellness Centre, {datetime.now().year}
        </div>
    </body>
    </html>
    """
    
    return complete_html

def create_pdf(markdown_content, user_data, output_filename=None):
    """
    Convert markdown wellness plan to PDF
    
    Args:
        markdown_content: Wellness plan in markdown format
        user_data: User information dictionary
        output_filename: Name for the output file (optional)
        
    Returns:
        Path to the generated PDF
    """
    try:
        # Generate output filename if not provided
        if not output_filename:
            user_name = user_data.get('Full Name', 'anonymous').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"wellness_plan_{user_name}_{timestamp}.pdf"
        
        # Ensure output directory exists
        output_dir = "generated_pdfs"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        
        # Convert markdown to HTML
        html_content = markdown_to_html(markdown_content, user_data)
        
        # Create a temporary file for HTML
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        # Configure fonts
        font_config = FontConfiguration()
        
        # Generate PDF from HTML
        HTML(filename=temp_html_path).write_pdf(
            output_path,
            font_config=font_config
        )
        
        # Clean up temporary HTML file
        os.unlink(temp_html_path)
        
        print(f"PDF generated successfully: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None

def get_sample_wellness_plan_path():
    """
    Returns the path to the sample_wellness_plan.md file
    Checks both app structure and root locations
    """
    # Option 1: App structure path
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'text_files', 'sample_wellness_plan.md')
    
    # Option 2: Root path
    root_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'text_files', 'sample_wellness_plan.md')
    
    # Check which one exists and return it
    if os.path.exists(root_path):
        return root_path
    else:
        return app_path

if __name__ == "__main__":
    # For testing
    sample_plan_path = get_sample_wellness_plan_path()
    with open(sample_plan_path, 'r', encoding='utf-8') as f:
        sample_content = f.read()
    
    user_data = {
        "Full Name": "Test User",
        "Email": "test@example.com",
        "WhatsApp Contact Number": "+91 9876543210"
    }
    
    create_pdf(sample_content, user_data) 
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import base64
import requests
import json

# Load environment variables
load_dotenv()

def send_email_with_attachment(recipient_email, subject, message, attachment_path=None):
    """
    Send an email with optional PDF attachment using Gmail SMTP
    
    Args:
        recipient_email: Email address of recipient
        subject: Email subject
        message: Email body text
        attachment_path: Path to PDF file to attach (optional)
    
    Returns:
        Boolean indicating success or failure
    """
    # First, try to use Google Apps Script method if webhook URL is configured
    webhook_url = os.environ.get('GOOGLE_APPS_SCRIPT_WEBHOOK')
    if webhook_url:
        try:
            return send_email_via_apps_script(
                recipient_email, subject, message, attachment_path, webhook_url
            )
        except Exception as e:
            print(f"Google Apps Script email failed: {str(e)}. Falling back to SMTP...")
    
    # Fallback to direct SMTP method
    try:
        # Get email credentials from environment variables
        sender_email = os.environ.get('GMAIL_USERNAME')
        sender_password = os.environ.get('GMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            raise ValueError("Gmail credentials not found in environment variables")
        
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Attach PDF if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read(), _subtype="pdf")
                attachment.add_header(
                    'Content-Disposition', 'attachment', 
                    filename=os.path.basename(attachment_path)
                )
                msg.attach(attachment)
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def send_email_via_apps_script(recipient_email, subject, message, attachment_path=None, webhook_url=None):
    """
    Send email using Google Apps Script webhook
    
    This method allows sending emails directly from Google account without needing
    to store passwords or enable less secure apps.
    """
    if not webhook_url:
        raise ValueError("Google Apps Script webhook URL not provided")
    
    # Prepare the payload
    payload = {
        "recipient": recipient_email,
        "subject": subject,
        "message": message,
    }
    
    # If attachment exists, encode it as base64
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            file_data = file.read()
            file_base64 = base64.b64encode(file_data).decode('utf-8')
            
            payload["attachment"] = {
                "data": file_base64,
                "filename": os.path.basename(attachment_path),
                "mimeType": "application/pdf"
            }
    
    # Send request to Google Apps Script webhook
    response = requests.post(
        webhook_url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        print(f"Email sent successfully via Google Apps Script to {recipient_email}")
        return True
    else:
        error_msg = response.text
        raise Exception(f"Failed to send email via Google Apps Script: {error_msg}")

if __name__ == "__main__":
    # For testing
    recipient = "test@example.com"
    subject = "Test Email from HRIM Wellness"
    message = "This is a test email with PDF attachment."
    attachment = "sample.pdf"  # Replace with an actual PDF path
    
    send_email_with_attachment(recipient, subject, message, attachment) 
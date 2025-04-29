import os
from twilio.rest import Client
from dotenv import load_dotenv
import requests
import tempfile
import json

# Load environment variables
load_dotenv()

def send_whatsapp_message(to_number, message, media_url=None):
    """
    Send WhatsApp message using Twilio API
    
    Args:
        to_number: Recipient's phone number with country code
        message: Message text to send
        media_url: URL or local path to media file (PDF)
        
    Returns:
        Message SID if successful, None otherwise
    """
    try:
        # Get Twilio credentials from environment variables
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        if not account_sid or not auth_token:
            raise ValueError("Twilio credentials not found in environment variables")
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Format WhatsApp numbers if needed
        if not to_number.startswith('whatsapp:'):
            # Remove any spaces or dashes from the phone number
            cleaned_number = ''.join(c for c in to_number if c.isdigit() or c == '+')
            to_number = f"whatsapp:{cleaned_number}"
        
        if not from_number.startswith('whatsapp:'):
            from_number = f"whatsapp:{from_number}"
        
        # If media_url is a local file path, upload it to temporary cloud storage
        if media_url and os.path.exists(media_url):
            # Upload the file to a publicly accessible URL
            # In a production environment, you'd use a proper cloud storage service
            # For this example, we'll use Twilio's media hosting
            media_url = upload_to_cloud_storage(media_url)
        
        # Send the message
        message_params = {
            'from_': from_number,
            'body': message,
            'to': to_number
        }
        
        # Add media if provided
        if media_url:
            message_params['media_url'] = [media_url]
        
        # Send the message
        twilio_message = client.messages.create(**message_params)
        
        print(f"WhatsApp message sent successfully. SID: {twilio_message.sid}")
        return twilio_message.sid
    
    except Exception as e:
        print(f"Failed to send WhatsApp message: {str(e)}")
        return None

def upload_to_cloud_storage(file_path):
    """
    Upload a file to temporary cloud storage
    
    In a production environment, replace this with uploading to:
    - Google Drive (since project uses Google Sheets)
    - AWS S3
    - Azure Blob Storage
    - Other cloud storage solution
    
    For this example, we'll use a temporary file hosting service.
    """
    # This is a placeholder. In a real environment, implement a proper upload mechanism
    # For testing purposes, use a service like file.io or similar temporary file hosts
    
    try:
        # For demo purposes - in production, replace with actual cloud storage API
        # This example uploads to file.io which provides temporary file hosting
        with open(file_path, 'rb') as file:
            response = requests.post(
                'https://file.io',
                files={'file': file}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and result.get('link'):
                    return result.get('link')
        
        # Fallback: return a placeholder URL
        return "https://example.com/yourfile.pdf"
    
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        # Return a placeholder URL
        return "https://example.com/yourfile.pdf"

if __name__ == "__main__":
    # For testing
    recipient = "+1234567890"  # Replace with actual phone number
    test_message = "Hello from HRIM Wellness! Your wellness plan is ready."
    test_media = "sample.pdf"  # Replace with actual PDF path
    
    send_whatsapp_message(recipient, test_message, test_media) 
import os
from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import re
import json
from fetch_sheet_data import fetch_user_data
from llm_integration import generate_wellness_plan
import tempfile
import time
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Simple in-memory cache for ongoing conversations and tracked questions
conversation_cache = {}
unknown_questions = {}

# Initialize Twilio client
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Owner's WhatsApp number to forward unexpected questions
OWNER_WHATSAPP_NUMBER = os.environ.get('OWNER_WHATSAPP_NUMBER')
TWILIO_WHATSAPP_NUMBER = os.environ.get('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

def forward_to_owner(customer_message, customer_number, customer_name=None):
    """Forward unexpected questions to the business owner's WhatsApp"""
    if not OWNER_WHATSAPP_NUMBER:
        print("No owner WhatsApp number configured for forwarding messages")
        return False
    
    # Format the WhatsApp numbers if needed
    owner_number = OWNER_WHATSAPP_NUMBER
    if not owner_number.startswith('whatsapp:'):
        owner_number = f"whatsapp:{owner_number}"
    
    from_number = TWILIO_WHATSAPP_NUMBER
    if not from_number.startswith('whatsapp:'):
        from_number = f"whatsapp:{from_number}"
    
    # Create a notification message for the owner
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notification = f"🔔 *NEW UNEXPECTED QUESTION*\n\nFrom: {customer_name or 'Unknown'} ({customer_number})\nTime: {timestamp}\n\nMessage: _{customer_message}_\n\nReply directly to this chat to respond to the customer."
    
    try:
        # Send the notification to the owner
        twilio_client.messages.create(
            from_=from_number,
            body=notification,
            to=owner_number
        )
        
        # Save this conversation for context
        if customer_number not in unknown_questions:
            unknown_questions[customer_number] = []
            
        unknown_questions[customer_number].append({
            'message': customer_message,
            'timestamp': timestamp,
            'forwarded': True
        })
        
        return True
    except Exception as e:
        print(f"Error forwarding message to owner: {str(e)}")
        return False

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    """Handle incoming WhatsApp messages via Twilio webhook"""
    # Get the incoming message details
    incoming_msg = request.values.get('Body', '').strip()
    incoming_msg_lower = incoming_msg.lower()
    sender = request.values.get('From', '')
    sender_name = request.values.get('ProfileName', 'Customer')
    
    # Create Twilio response
    resp = MessagingResponse()
    msg = resp.message()
    
    # Check if this is a message status update
    if 'SmsStatus' in request.form:
        print(f"Message status update: {request.form.get('SmsStatus')} for {sender}")
        return str(resp)
    
    # Check if this is a message from the owner to a customer
    if sender.replace('whatsapp:', '') == OWNER_WHATSAPP_NUMBER.replace('whatsapp:', ''):
        # This is the owner responding to a customer
        # Check if this is a reply to a forwarded message
        if request.values.get('Body', '').strip().startswith('Reply to:'):
            # Parse the customer number from the message
            parts = request.values.get('Body', '').strip().split('\n', 2)
            if len(parts) >= 2:
                customer_number = parts[1].strip()
                response_message = parts[2].strip() if len(parts) > 2 else "Thank you for your question. Our team will assist you shortly."
                
                # Format customer number if needed
                if not customer_number.startswith('whatsapp:'):
                    customer_number = f"whatsapp:{customer_number}"
                
                # Send the owner's response to the customer
                try:
                    twilio_client.messages.create(
                        from_=TWILIO_WHATSAPP_NUMBER if not TWILIO_WHATSAPP_NUMBER.startswith('whatsapp:') else TWILIO_WHATSAPP_NUMBER,
                        body=response_message,
                        to=customer_number
                    )
                    msg.body("Response sent to customer.")
                except Exception as e:
                    msg.body(f"Error sending response: {str(e)}")
            else:
                msg.body("Invalid format. Please use:\nReply to:\n<customer_number>\n<your message>")
        else:
            # Direct owner message, just acknowledge
            msg.body("Message received. To reply to a customer, start with 'Reply to:' followed by their number.")
        
        return str(resp)
    
    # Process regular customer commands
    if incoming_msg_lower in ['hi', 'hello', 'start']:
        msg.body("Hello! Welcome to HRIM Wellness Centre. How can I help you today?\n\n"
                 "1. Check my plan status\n"
                 "2. Request a new plan\n"
                 "3. Contact a dietician\n"
                 "4. FAQ\n\n"
                 "Please type the number of your choice or the keyword.")
        
    elif incoming_msg_lower == '1' or 'status' in incoming_msg_lower or 'check' in incoming_msg_lower:
        # Extract phone number from WhatsApp format
        phone_number = sender.replace('whatsapp:', '')
        user_data = fetch_user_data(filter_phone=phone_number)
        
        if user_data and len(user_data) > 0:
            user = user_data[0]
            name = user.get('Full Name', 'there')
            msg.body(f"Hello {name}! Your wellness plan is being processed. "
                     f"We'll send it to you as soon as it's ready. "
                     f"Thank you for your patience!")
        else:
            msg.body("We couldn't find any submission associated with this phone number. "
                     "Please fill out our form first at: https://forms.gle/yourFormLink")
    
    elif incoming_msg_lower == '2' or 'request' in incoming_msg_lower or 'new plan' in incoming_msg_lower:
        # Send the Google Form link
        form_link = os.environ.get('GOOGLE_FORM_LINK', 'https://forms.gle/yourFormLink')
        msg.body(f"To request a new wellness plan, please fill out our form at:\n\n{form_link}")
    
    elif incoming_msg_lower == '3' or 'contact' in incoming_msg_lower or 'dietician' in incoming_msg_lower:
        # Provide contact information
        msg.body("For personalized assistance, you can contact our dietician directly:\n\n"
                "📞 +91 94279 81235\n"
                "📧 hrimwellness@gmail.com\n\n"
                "Our office hours are 9AM-6PM IST, Monday through Saturday.")
    
    elif incoming_msg_lower == '4' or 'faq' in incoming_msg_lower:
        # Send FAQ
        msg.body("Frequently Asked Questions:\n\n"
                "Q: How long does it take to receive my wellness plan?\n"
                "A: Typically 1-2 business days after form submission.\n\n"
                "Q: Are follow-up consultations available?\n"
                "A: Yes, you can schedule them by contacting us.\n\n"
                "Q: How personalized is the plan?\n"
                "A: Each plan is completely customized based on your form responses.\n\n"
                "For more questions, contact us at +91 94279 81235.")
    
    elif 'help' in incoming_msg_lower:
        # Help menu
        msg.body("HRIM Wellness Chatbot Help:\n\n"
                "- Type 'status' to check your plan status\n"
                "- Type 'request' to request a new plan\n"
                "- Type 'contact' to get support contact info\n"
                "- Type 'faq' for frequently asked questions\n\n"
                "If you need immediate assistance, contact us at +91 94279 81235.")
    
    else:
        # This is an unexpected question - forward to owner
        is_forwarded = forward_to_owner(incoming_msg, sender, sender_name)
        
        if is_forwarded:
            # Let the user know their message has been forwarded
            msg.body("Thank you for your message. Our team will review it and get back to you soon.")
        else:
            # Default response if forwarding fails
            msg.body("I'm not sure how to respond to that. Please try one of these commands:\n\n"
                    "- Type '1' to check plan status\n"
                    "- Type '2' to request a new wellness plan\n"
                    "- Type '3' to contact a dietician\n"
                    "- Type '4' for FAQ\n"
                    "- Type 'help' for more options\n\n"
                    "Or contact us directly at +91 94279 81235.")
    
    return str(resp)

@app.route("/files/<filename>", methods=['GET'])
def serve_file(filename):
    """Serve PDF files to WhatsApp users"""
    file_path = os.path.join('generated_pdfs', filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/pdf')
    else:
        return "File not found", 404

def run_webhook_server():
    """Run the Flask webhook server"""
    # Get configuration from environment variables
    host = os.environ.get('WEBHOOK_HOST', '0.0.0.0')
    port = int(os.environ.get('WEBHOOK_PORT', 5000))
    debug = os.environ.get('WEBHOOK_DEBUG', 'False').lower() == 'true'
    
    # Run the Flask app
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    run_webhook_server() 
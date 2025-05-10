import os
import json
from dotenv import load_dotenv
import time
from datetime import datetime

# Import component modules
from fetch_sheet_data import fetch_user_data
from llm_integration import generate_wellness_plan
from generate_pdf import create_pdf
from send_email import send_email_with_attachment
from send_whatsapp import send_whatsapp_message

# Load environment variables
load_dotenv()

def process_user(user_data):
    """Process a single user's data through the entire workflow"""
    
    user_email = user_data.get('Email')
    user_name = user_data.get('Full Name', 'User')
    user_phone = user_data.get('WhatsApp Contact Number')
    
    print(f"Processing wellness plan for: {user_name} ({user_email})")
    
    # Step 1: Generate wellness plan using LLM
    wellness_plan = generate_wellness_plan(user_data)
    
    # Step 2: Generate PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wellness_plan_{user_name.replace(' ', '_')}_{timestamp}.pdf"
    pdf_path = create_pdf(wellness_plan, user_data, filename)
    
    # Step 3: Send via email if email is provided
    if user_email:
        try:
            send_email_with_attachment(
                recipient_email=user_email,
                subject="Your Personalized Wellness Plan - HRIM Wellness",
                message=f"Dear {user_name},\n\nThank you for using HRIM Wellness Centre's services. Please find your personalized wellness plan attached.\n\nWishing you good health,\nHRIM Wellness Team",
                attachment_path=pdf_path
            )
            print(f"Email sent successfully to {user_email}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
    
    # Step 4: Send via WhatsApp if phone number is provided
    if user_phone:
        try:
            send_whatsapp_message(
                to_number=user_phone,
                message=f"Dear {user_name}, your personalized wellness plan from HRIM Wellness Centre is ready!",
                media_url=pdf_path if os.path.exists(pdf_path) else None
            )
            print(f"WhatsApp message sent successfully to {user_phone}")
        except Exception as e:
            print(f"Failed to send WhatsApp message: {str(e)}")
    
    return {
        "user_name": user_name,
        "email": user_email,
        "phone": user_phone,
        "pdf_path": pdf_path,
        "timestamp": timestamp
    }

def main():
    # Step 1: Fetch new submissions from Google Sheets
    print("Fetching user data from Google Sheets...")
    user_data_list = fetch_user_data()
    
    if not user_data_list:
        print("No new user data found.")
        return
    
    print(f"Found {len(user_data_list)} users to process.")
    
    # Step 2: Process each user
    results = []
    for user_data in user_data_list:
        try:
            result = process_user(user_data)
            results.append(result)
            # Add a delay to avoid rate limiting with LLM API
            time.sleep(2)
        except Exception as e:
            print(f"Error processing user {user_data.get('Email', 'unknown')}: {str(e)}")
    
    # Step 3: Save processing log
    log_file = f"processing_log_{datetime.now().strftime('%Y%m%d')}.json"
    with open(log_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Processed {len(results)} users. Log saved to {log_file}")

if __name__ == "__main__":
    main() 
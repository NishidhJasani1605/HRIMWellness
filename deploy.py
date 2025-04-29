#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path
import json
import re

# ANSI colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_header(message):
    """Print a formatted header message"""
    print(f"\n{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}==  {message}{' ' * (76 - len(message))}=={RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}\n")

def print_success(message):
    """Print a success message"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_warning(message):
    """Print a warning message"""
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_error(message):
    """Print an error message"""
    print(f"{RED}✗ {message}{RESET}")

def print_step(message):
    """Print a step message"""
    print(f"  • {message}")

def check_environment():
    """Check if the environment is properly set up"""
    print_header("Checking Environment")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print_error(f"Python 3.8+ is required. Found: {python_version.major}.{python_version.minor}")
        return False
    else:
        print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    
    # Check for pip
    try:
        subprocess.check_output(["pip", "--version"])
        print_success("pip is installed")
    except:
        print_error("pip is not installed or not in the PATH")
        return False
    
    # Check for virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print_success("Running in a virtual environment")
    else:
        print_warning("Not running in a virtual environment. It's recommended to use one.")
    
    # Check for .env file
    if os.path.exists(".env"):
        print_success(".env file found")
    else:
        print_warning(".env file not found, will create template")
        with open(".env.template", "w") as f:
            f.write("""OPENAI_API_KEY=your_openai_api_key
GOOGLE_SHEET_NAME=Your Google Sheet Name
USER_EMAIL=user@example.com
USER_PHONE=+1234567890
GMAIL_USERNAME=your_email@gmail.com
GMAIL_PASSWORD=your_password
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=+14155238886
OWNER_WHATSAPP_NUMBER=+911234567890
GOOGLE_FORM_LINK=https://forms.gle/yourFormLink
GOOGLE_APPS_SCRIPT_WEBHOOK=https://script.google.com/macros/s/your-webhook-id/exec
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=5000
WEBHOOK_DEBUG=False""")
        print_step("Created .env.template - Rename to .env and fill in your values")
    
    # Check for credentials.json file
    if os.path.exists("credentials.json"):
        print_success("Google API credentials.json found")
    else:
        print_warning("credentials.json not found. You'll need this for Google Sheets integration.")
        print_step("Create a service account key at: https://console.cloud.google.com/apis/credentials")
    
    return True

def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("Successfully installed all dependencies")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {str(e)}")
        return False

def setup_directories():
    """Create necessary directories"""
    print_header("Setting Up Project Directories")
    
    dirs = ["generated_pdfs", "logs"]
    
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print_success(f"Created directory: {directory}")
        else:
            print_step(f"Directory already exists: {directory}")
    
    return True

def test_components():
    """Test individual components"""
    print_header("Testing Components")
    
    # Test environment variables loading
    try:
        from dotenv import load_dotenv
        load_dotenv()
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_api_key":
            print_success("Environment variables loaded successfully")
        else:
            print_warning("OpenAI API key not set or using default value")
    except ImportError:
        print_error("Failed to import dotenv")
    
    # Test Google Sheets connection
    try:
        print_step("Testing Google Sheets connection...")
        from fetch_sheet_data import fetch_user_data
        fetch_user_data(filter_email="test@example.com")  # This won't return anything but should run
        print_success("Google Sheets module loaded successfully")
    except Exception as e:
        print_error(f"Google Sheets connection failed: {str(e)}")
    
    # Test OpenAI connection
    try:
        print_step("Testing OpenAI connection...")
        import openai
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if openai.api_key:
            print_success("OpenAI API key loaded")
        else:
            print_error("OpenAI API key not found")
    except ImportError:
        print_error("Failed to import OpenAI module")
    
    # Test Twilio connection
    try:
        print_step("Testing Twilio connection...")
        from twilio.rest import Client
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        if account_sid and auth_token and account_sid != "your_account_sid":
            print_success("Twilio credentials loaded")
        else:
            print_warning("Twilio credentials not set or using default values")
    except ImportError:
        print_error("Failed to import Twilio module")
    
    return True

def run_flask_app(debug=False):
    """Run the Flask webhook server"""
    print_header("Starting WhatsApp Chatbot Server")
    
    try:
        from whatsapp_chatbot import run_webhook_server
        print_success("Starting Flask server...")
        run_webhook_server()
    except ImportError as e:
        print_error(f"Failed to import webhook server: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Failed to start webhook server: {str(e)}")
        return False
    
    return True

def main():
    """Main deployment function"""
    print_header("HRIM Wellness Deployment")
    
    print("This script will help you set up the HRIM Wellness system.\n")
    
    # Step 1: Check environment
    if not check_environment():
        print_error("Environment check failed. Please fix the issues and try again.")
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print_error("Failed to install dependencies. Please fix the issues and try again.")
        return
    
    # Step 3: Setup directories
    if not setup_directories():
        print_error("Failed to set up directories. Please fix the issues and try again.")
        return
    
    # Step 4: Test components
    if not test_components():
        print_warning("Some components failed testing. You may need to fix these issues.")
        proceed = input("Do you want to proceed anyway? (y/n): ").lower()
        if proceed != 'y':
            return
    
    # Step 5: Ask about running the server
    run_server = input("Do you want to start the WhatsApp webhook server now? (y/n): ").lower()
    if run_server == 'y':
        debug_mode = input("Run in debug mode? (y/n): ").lower() == 'y'
        run_flask_app(debug=debug_mode)
    else:
        print_step("To run the server later, use: python whatsapp_chatbot.py")
    
    print_header("Deployment Complete")
    print("Thank you for using the HRIM Wellness system!")
    print("\nNext steps:")
    print("  1. Fill in your .env file with your API keys and settings")
    print("  2. Ensure your Google Sheets form is properly set up")
    print("  3. Test the workflow with a sample user")
    print("  4. Expose your webhook server with ngrok or similar for Twilio to reach it")
    print("\nFor more information, refer to the README.md file.")

if __name__ == "__main__":
    main() 
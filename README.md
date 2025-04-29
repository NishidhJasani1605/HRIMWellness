# HRIMWellness

## Overview
HRIMWellness is an automated system designed to generate personalized diet and wellness plans based on user input collected via Google Forms. The system leverages OpenAI GPT-4-turbo to analyze user data and create detailed, research-backed wellness reports in PDF format, which can be delivered to users via email or WhatsApp.

## Features
- Collects user data through Google Forms and stores it in Google Sheets
- Fetches and formats user data automatically
- Integrates with OpenAI GPT-4-turbo for advanced plan generation
- Generates professional PDF reports for each user
- Sends reports via email (using Google Apps Script) and WhatsApp (Twilio)
- Interactive WhatsApp chatbot for user inquiries
- Forwards unexpected user questions to the owner's WhatsApp for personalized responses

## Project Structure
```
├── automate_workflow.py      # Main automation script
├── fetch_sheet_data.py       # Fetches data from Google Sheets
├── llm_integration.py        # Sends data to OpenAI API
├── generate_pdf.py           # Generates PDF reports
├── send_email.py             # Sends PDF via email
├── send_whatsapp.py          # Sends PDF via WhatsApp
├── whatsapp_chatbot.py       # WhatsApp chatbot integration
├── apps_script_email.js      # Google Apps Script for email delivery
├── form_structure.txt        # Google Form structure
├── llm_prompt.txt            # LLM prompt template
├── requirements.txt          # Python dependencies
├── deploy.py                 # Deployment and setup script
├── .env                      # Environment variables (not tracked)
├── credentials.json          # Google API credentials (not tracked)
└── README.md                 # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/NishidhJasani1605/HRIMWellness.git
   cd HRIMWellness
   ```
2. **Use the deployment script for easy setup:**
   ```bash
   python deploy.py
   ```
   This script will:
   - Check your environment for required software
   - Install dependencies
   - Create necessary directories
   - Test the components
   - Optionally start the WhatsApp chatbot server
3. **Manual setup (if not using deploy.py):**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up Google Sheets API:**
   - Create a Google Cloud project and enable the Google Sheets API.
   - Download `credentials.json` and place it in the project root.
5. **Configure environment variables:**
   - Create a `.env` file with your API keys and settings:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     GOOGLE_SHEET_NAME=Your Google Sheet Name
     GMAIL_USERNAME=your_email@gmail.com
     GMAIL_PASSWORD=your_password
     TWILIO_ACCOUNT_SID=your_account_sid
     TWILIO_AUTH_TOKEN=your_auth_token
     TWILIO_WHATSAPP_NUMBER=+14155238886
     OWNER_WHATSAPP_NUMBER=+911234567890
     GOOGLE_FORM_LINK=https://forms.gle/yourFormLink
     WEBHOOK_HOST=0.0.0.0
     WEBHOOK_PORT=5000
     ```
6. **Set up WhatsApp Business API with Twilio:**
   - Create a Twilio account and set up a WhatsApp Sandbox
   - Configure the webhook URL to point to your server: `https://your-domain.com/whatsapp`
   - Test your WhatsApp integration by sending a message to your Twilio number

## Usage

### Automated Workflow
To process new form submissions and generate plans:
```bash
python automate_workflow.py
```

### WhatsApp Chatbot
To start the WhatsApp chatbot server:
```bash
python whatsapp_chatbot.py
```

You'll need to expose your webhook server to the internet using a service like ngrok:
```bash
ngrok http 5000
```

Then set the Twilio WhatsApp webhook to the provided ngrok URL + `/whatsapp`.

### WhatsApp Chatbot Features
The WhatsApp chatbot supports these commands:
- **Start/Hello/Hi** - Display the welcome menu
- **1 or "status"** - Check wellness plan status
- **2 or "request"** - Request a new wellness plan (sends form link)
- **3 or "contact"** - Get contact information for a dietician
- **4 or "FAQ"** - View frequently asked questions
- **help** - Display help menu

### Unexpected Questions Handling
When users ask questions not covered by the predefined commands:
1. The question is automatically forwarded to the owner's WhatsApp
2. The owner receives a notification with the user's question and contact details
3. The owner can respond directly to the customer using the format:
   ```
   Reply to:
   <customer_number>
   <your response message>
   ```
4. The system will send the owner's response back to the customer

## Security & Best Practices
- **Never commit your `.env` or `credentials.json` files.**
- Review all generated plans for accuracy before sharing with users.
- Ensure compliance with privacy and data protection regulations.
- Regularly monitor logs and unexpected questions to improve the system.
- Set up rate limiting to prevent abuse of the OpenAI API.

## Google Apps Script Integration
- Use the provided `apps_script_email.js` as a template for your Google Apps Script
- Deploy as a web app with access set to "Anyone, even anonymous"
- Set the deployed URL in the `.env` file as `GOOGLE_APPS_SCRIPT_WEBHOOK`

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, contact:
- HRIM Wellness Centre, Surat
- 📧 hrimwellness@gmail.com
- 🌐 [www.hrimwellness.in](http://www.hrimwellness.in)
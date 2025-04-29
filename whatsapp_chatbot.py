from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    # Process with LLM if needed
    resp = MessagingResponse()
    resp.message("Your automated reply here")
    return str(resp)

if __name__ == "__main__":
    app.run() 
from twilio.rest import Client

# Set your Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

# Send WhatsApp message with PDF link
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Here is your PDF',
    to='whatsapp:+user_number',
    media_url='https://your-server.com/output.pdf'
) 
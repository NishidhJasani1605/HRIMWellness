import yagmail

# Set your Gmail credentials
yag = yagmail.SMTP('your_email@gmail.com', 'your_password')

# Send email with PDF attachment
yag.send(
    to='recipient_email@example.com',
    subject='Your PDF',
    contents='Here is your PDF',
    attachments='output.pdf'
) 
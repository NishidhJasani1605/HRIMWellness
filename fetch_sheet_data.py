import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope for Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from the JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by its name
sheet = client.open("Your Google Sheet Name").sheet1

# Fetch all records from the sheet
data = sheet.get_all_records()

# Filter data based on email or phone number
user_email = "user@example.com"  # Replace with actual email
user_phone = "+1234567890"  # Replace with actual phone number

filtered_data = [row for row in data if row.get('Email') == user_email or row.get('Phone') == user_phone]
print(filtered_data) 
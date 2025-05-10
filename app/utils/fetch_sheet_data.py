import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_user_data(processed_flag_column="Processed", filter_email=None, filter_phone=None):
    """
    Fetch user data from Google Sheets.
    
    Args:
        processed_flag_column: Column name to mark as processed
        filter_email: Optional email to filter specific user
        filter_phone: Optional phone number to filter specific user
        
    Returns:
        List of dictionaries containing user data
    """
    try:
        # Define the scope for Google Sheets API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Load credentials from the JSON file
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        # Open the Google Sheet by its name from environment variable
        sheet_name = os.environ.get('GOOGLE_SHEET_NAME', 'Default Sheet Name')
        sheet = client.open(sheet_name).sheet1
        
        # Fetch all records from the sheet
        all_records = sheet.get_all_records()
        
        # Filter unprocessed records or specific user if email/phone provided
        if filter_email or filter_phone:
            # Filter by email or phone if provided
            filtered_data = [
                row for row in all_records 
                if (filter_email and row.get('Email') == filter_email) or 
                   (filter_phone and row.get('WhatsApp Contact Number') == filter_phone)
            ]
        else:
            # Filter only unprocessed records
            filtered_data = [
                row for row in all_records 
                if not row.get(processed_flag_column, False)
            ]
            
            # Mark these records as processed
            if filtered_data and processed_flag_column in sheet.row_values(1):
                # Get the column index for the processed flag
                header_row = sheet.row_values(1)
                processed_col_idx = header_row.index(processed_flag_column) + 1  # 1-indexed
                
                # Mark each row as processed
                for row in filtered_data:
                    # Find the row index in the sheet
                    for i, record in enumerate(all_records, start=2):  # Start from row 2 (after header)
                        if record.get('Email') == row.get('Email') and record.get('Timestamp') == row.get('Timestamp'):
                            sheet.update_cell(i, processed_col_idx, True)
                            break
        
        # Post-process the data to ensure consistent formatting
        for record in filtered_data:
            # Convert height from cm to m for BMI calculation
            if 'Height (in cm)' in record:
                try:
                    height_cm = float(record['Height (in cm)'])
                    record['Height (m)'] = height_cm / 100.0
                except (ValueError, TypeError):
                    record['Height (m)'] = None
            
            # Parse date of birth to age if present
            if 'Date of Birth' in record:
                # Add age parsing logic here if needed
                pass
                
        return filtered_data
    
    except Exception as e:
        print(f"Error fetching data from Google Sheets: {str(e)}")
        return []

if __name__ == "__main__":
    # For testing purposes
    user_data = fetch_user_data()
    print(f"Found {len(user_data)} unprocessed records")
    for user in user_data:
        print(f"User: {user.get('Full Name', 'Unknown')}, Email: {user.get('Email', 'No email')}") 
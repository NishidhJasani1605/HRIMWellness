import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print all environment variables
print("Environment variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

# Check specific variable
cohere_api_key = os.getenv('q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh')
print("\nCOHERE_API_KEY:")
if cohere_api_key:
    print(f"Found: {cohere_api_key}")
else:
    print("Not found")

# Try to read the .env file directly
print("\nReading .env file directly:")
try:
    with open('.env', 'r') as f:
        env_contents = f.read()
        print(env_contents)
except Exception as e:
    print(f"Error reading .env file: {str(e)}") 
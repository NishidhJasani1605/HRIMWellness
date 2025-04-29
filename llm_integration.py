import openai

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Example user data (replace with actual data from Google Sheets)
user_data = "Sample user data"

# Construct your prompt
prompt = f"Your custom prompt with user data: {user_data}"

# Send prompt to OpenAI API
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

# Extract the response
answer = response['choices'][0]['message']['content']
print(answer) 
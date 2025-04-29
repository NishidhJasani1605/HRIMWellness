import openai

# Read your prompt
with open('llm_prompt.txt', 'r', encoding='utf-8') as f:
    base_prompt = f.read()

# Example: formatted patient data (replace with your actual data extraction)
patient_data = """
Full Name: John Doe
Date of Birth: 01/01/1980
Gender: Male
...
"""

# Combine prompt and patient data
full_prompt = f"{base_prompt}\n\nPatient Data:\n{patient_data}"

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Call GPT-4-turbo
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": full_prompt}]
)
plan = response['choices'][0]['message']['content']

# Save or process the plan as needed
with open("output_plan.txt", "w", encoding="utf-8") as out:
    out.write(plan) 
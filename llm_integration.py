import os
import openai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

def format_user_data(user_data):
    """Format user data into a structured string for the LLM prompt"""
    formatted_data = []
    
    # Personal details section
    personal_fields = [
        "Full Name", "Date of Birth", "Gender", "WhatsApp Contact Number",
        "City", "State", "Country", "Occupation", "Marital Status"
    ]
    
    formatted_data.append("# Personal Details")
    for field in personal_fields:
        if field in user_data and user_data[field]:
            formatted_data.append(f"{field}: {user_data[field]}")
    
    # Health metrics section
    health_fields = [
        "Height (in cm)", "Current Weight (in kg)", "Target Weight (if any)",
        "Primary Health Goals"
    ]
    
    formatted_data.append("\n# Health Metrics")
    for field in health_fields:
        if field in user_data and user_data[field]:
            formatted_data.append(f"{field}: {user_data[field]}")
    
    # Medical history section
    medical_fields = [
        "Do you have any existing medical conditions?",
        "If yes, please specify medical conditions",
        "Are you currently on any medication?",
        "Any allergies (food or otherwise)?",
        "If yes, please specify allergies",
        "Family Medical History"
    ]
    
    formatted_data.append("\n# Medical History")
    for field in medical_fields:
        if field in user_data and user_data[field]:
            formatted_data.append(f"{field}: {user_data[field]}")
    
    # Daily routine section
    routine_fields = [
        "Wake-Up Time", "Sleep Time", "Average Hours of Sleep",
        "Work Schedule", "Physical Activity Level", "Exercise Routine (if any)",
        "Stress Levels", "Screen Time per Day (Hours)"
    ]
    
    formatted_data.append("\n# Daily Routine")
    for field in routine_fields:
        if field in user_data and user_data[field]:
            formatted_data.append(f"{field}: {user_data[field]}")
    
    # Dietary preferences section
    diet_fields = [
        "Dietary Preference", "Any Dietary Restrictions?",
        "If yes, please specify Dietary Restrictions", "Meals Per Day",
        "Snacking Habit", "Water Intake Per Day (in Liters)",
        "Consumption of Caffeine (Tea/Coffee) Cups Per Day",
        "Frequency of Eating Out"
    ]
    
    formatted_data.append("\n# Dietary Preferences")
    for field in diet_fields:
        if field in user_data and user_data[field]:
            formatted_data.append(f"{field}: {user_data[field]}")
    
    # Mental wellbeing section
    mental_fields = [
        "How often do you feel stressed?",
        "Do you practice any relaxation techniques?",
        "If yes, specify relaxation techniques",
        "Hobbies and Leisure Activities (Describe)"
    ]
    
    formatted_data.append("\n# Mental & Emotional Wellbeing")
    for field in mental_fields:
        if field in user_data and user_data[field]:
            formatted_data.append(f"{field}: {user_data[field]}")
    
    # Goals and concerns section
    goals_fields = [
        "Any specific concerns or goals you would like to address?",
        "Have you followed any diet or fitness plan before?",
        "If yes, what type and what were the results?"
    ]
    
    formatted_data.append("\n# Goals & Concerns")
    for field in goals_fields:
        if field in user_data and user_data[field]:
            formatted_data.append(f"{field}: {user_data[field]}")
    
    return "\n".join(formatted_data)

def generate_wellness_plan(user_data):
    """Generate a wellness plan using GPT-4-turbo"""
    try:
        # Read the base prompt template
        with open('llm_prompt.txt', 'r', encoding='utf-8') as f:
            base_prompt = f.read()
        
        # Format the user data
        formatted_user_data = format_user_data(user_data)
        
        # Combine the base prompt with the user data
        full_prompt = f"{base_prompt}\n\nPatient Data:\n{formatted_user_data}"
        
        # Make the API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Using GPT-4-turbo for best medical reasoning
            messages=[
                {"role": "system", "content": "You are an expert clinical dietician with extensive experience in wellness planning."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        # Extract the generated plan
        wellness_plan = response['choices'][0]['message']['content']
        
        # Save a copy of the generated plan for record-keeping
        user_name = user_data.get('Full Name', 'anonymous').replace(' ', '_')
        with open(f"generated_plan_{user_name}.md", "w", encoding="utf-8") as f:
            f.write(wellness_plan)
        
        return wellness_plan
    
    except Exception as e:
        print(f"Error generating wellness plan: {str(e)}")
        return f"Error generating wellness plan: {str(e)}"

if __name__ == "__main__":
    # For testing purposes
    sample_data = {
        "Full Name": "Test User",
        "Date of Birth": "01/01/1980",
        "Gender": "Female",
        "Height (in cm)": "165",
        "Current Weight (in kg)": "70",
        "Primary Health Goals": "Weight Loss",
        "Dietary Preference": "Vegetarian",
        "State": "Gujarat"
    }
    
    plan = generate_wellness_plan(sample_data)
    print("Plan generated successfully.") 
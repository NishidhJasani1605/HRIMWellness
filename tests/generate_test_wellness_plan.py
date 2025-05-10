import os
import sys
import random
import json
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules
from app.api.cohere_integration import generate_wellness_plan
# Commented out due to import errors - not directly used in this file
# from app.core.wellness.generate_wellness_pdf import process_form_data

def generate_random_time():
    """Generate a random time in HH:MM AM/PM format"""
    hour = random.randint(1, 12)
    minute = random.choice([0, 15, 30, 45])
    am_pm = random.choice(["AM", "PM"])
    return f"{hour}:{minute:02d} {am_pm}"

def generate_random_date():
    """Generate a random date of birth for an adult (20-60 years old)"""
    today = datetime.now()
    age = random.randint(20, 60)
    birth_date = today - timedelta(days=365 * age + random.randint(0, 364))
    return birth_date.strftime("%Y-%m-%d")

def generate_random_form_data():
    """Generate random form data based on form_structure.txt"""
    # Find text_files directory
    if os.path.exists('text_files'):
        text_files_dir = 'text_files'
    else:
        text_files_dir = os.path.join('app', 'data', 'text_files')
    
    # Names data
    first_names = ["Amit", "Priya", "Raj", "Neha", "Vikram", "Meera", "Sanjay", "Deepa", "Arjun", "Kavita"]
    last_names = ["Patel", "Shah", "Sharma", "Desai", "Mehta", "Joshi", "Singh", "Verma", "Kumar", "Gandhi"]
    
    # Cities in Gujarat
    gujarat_cities = ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar", "Bhavnagar", "Jamnagar", "Junagadh", "Anand", "Navsari"]
    
    # Health goals
    health_goals = ["Weight Loss", "Weight Gain", "Manage Chronic Disease", "Improve Fitness & Stamina", "Boost Immunity", "Stress Management"]
    
    # Medical conditions
    medical_conditions = ["Diabetes", "Hypertension", "Thyroid disorder", "High cholesterol", "None", "Asthma"]
    
    # Dietary preferences
    dietary_preferences = ["Vegetarian", "Non-Vegetarian", "Mixed Diet", "Vegan", "Gluten free", "Jain"]
    
    # Generate form data
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    city = random.choice(gujarat_cities)
    
    # Generate random height (150-190 cm) and weight (50-90 kg)
    height = random.randint(150, 190)
    current_weight = random.randint(50, 90)
    
    # Target weight is either slightly less or more than current weight
    weight_change = random.randint(-15, 15)
    target_weight = current_weight + weight_change if weight_change != 0 else ""
    
    # Random health goals (1-3 goals)
    num_goals = random.randint(1, 3)
    selected_goals = random.sample(health_goals, num_goals)
    
    # Medical condition
    has_medical_condition = random.choice(["Yes", "No"])
    if has_medical_condition == "Yes":
        medical_condition = random.choice(medical_conditions)
    else:
        medical_condition = ""
    
    # Generate the form data
    form_data = {
        "Email": f"{name.lower().replace(' ', '.')}@example.com",
        "Full Name": name,
        "Date of Birth": generate_random_date(),
        "Gender": random.choice(["Male", "Female"]),
        "WhatsApp Contact Number": f"+91 {random.randint(7000000000, 9999999999)}",
        "Address": f"{random.randint(1, 100)}, Some Street",
        "City": city,
        "PIN": f"{random.randint(380001, 399999)}",
        "State": "Gujarat",
        "Country": "India",
        "Occupation": random.choice(["Software Engineer", "Teacher", "Doctor", "Business Owner", "Student", "Accountant"]),
        "Marital Status": random.choice(["Single", "Married", "Other"]),
        "Height (in cm)": str(height),
        "Current Weight (in kg)": str(current_weight),
        "Target Weight (if any)": str(target_weight) if target_weight else "",
        "Primary Health Goals": ", ".join(selected_goals),
        "Do you have any existing medical conditions?": has_medical_condition,
        "If yes, please specify medical conditions": medical_condition,
        "Are you currently on any medication?": random.choice(["Yes", "No"]),
        "Any allergies (food or otherwise)?": random.choice(["Yes", "No"]),
        "If yes, please specify allergies": random.choice(["Nuts", "Seafood", "Dairy", "Pollen", ""]),
        "Family Medical History": random.choice(["Diabetes", "Heart disease", "Hypertension", "None known"]),
        "Wake-Up Time": generate_random_time(),
        "Sleep Time": generate_random_time(),
        "Average Hours of Sleep": str(random.randint(5, 9)),
        "Work Schedule": random.choice(["Fixed", "Rotational", "Remote", "Field Work", "Other"]),
        "Physical Activity Level": random.choice(["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]),
        "Exercise Routine (if any)": random.choice(["Walking daily", "Gym 3 times a week", "Yoga", "No regular exercise"]),
        "Stress Levels": random.choice(["Low", "Moderate", "High"]),
        "Screen Time per Day (Hours)": str(random.randint(2, 10)),
        "Dietary Preference": random.choice(dietary_preferences),
        "Any Dietary Restrictions?": random.choice(["Yes", "No"]),
        "If yes, please specify Dietary Restrictions": random.choice(["No onion", "No garlic", "No dairy", ""]),
        "Meals Per Day": random.choice(["2", "3", "4", "More"]),
        "Snacking Habit": random.choice(["Yes", "No", "Occasionally"]),
        "Water Intake Per Day (in Liters)": str(random.randint(1, 4)),
        "Consumption of Caffeine (Tea/Coffee) Cups Per Day": str(random.randint(0, 5)),
        "Frequency of Eating Out": random.choice(["Rarely", "Weekly", "Monthly", "Frequently"]),
        "How often do you feel stressed?": random.choice(["Rarely", "Sometimes", "Often"]),
        "Do you practice any relaxation techniques?": random.choice(["Yes", "No"]),
        "If yes, specify relaxation techniques": random.choice(["Meditation", "Deep breathing", "Yoga", ""]),
        "Hobbies and Leisure Activities (Describe)": random.choice(["Reading", "Cooking", "Gardening", "Playing sports", "Watching movies"]),
        "Any specific concerns or goals you would like to address?": random.choice(["Reduce belly fat", "Improve energy levels", "Better sleep", "Reduce stress"]),
        "Have you followed any diet or fitness plan before?": random.choice(["Yes", "No"]),
        "If yes, what type and what were the results?": random.choice(["Keto diet, lost 5kg but gained back", "Intermittent fasting with good results", ""]),
    }
    
    return form_data

def generate_and_display_wellness_plan():
    """Generate a wellness plan using random form data and display it"""
    print("Generating random form data...")
    form_data = generate_random_form_data()
    
    print(f"Generated form data for: {form_data['Full Name']}")
    print(f"Primary Health Goals: {form_data['Primary Health Goals']}")
    print(f"Dietary Preference: {form_data['Dietary Preference']}")
    
    print("\nGenerating wellness plan...")
    
    # Option 1: Using the llm_integration module directly
    wellness_plan = generate_wellness_plan(form_data)
    
    # Option 2: Using the process_form_data function which handles PDF generation
    # output_path = process_form_data(form_data)
    # print(f"Plan saved to: {output_path}")
    
    # Display the first 500 characters of the wellness plan
    if wellness_plan:
        print("\nWellness Plan Preview (first 500 characters):")
        print(wellness_plan[:500] + "...\n")
        print(f"Total characters in wellness plan: {len(wellness_plan)}")
    else:
        print("Failed to generate wellness plan.")

if __name__ == "__main__":
    print("=== HRIM Wellness Plan Generator ===")
    generate_and_display_wellness_plan() 
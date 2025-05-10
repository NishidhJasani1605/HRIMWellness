import cohere_integration as ci
import json
import argparse
import os
from datetime import datetime

def load_profile_from_file(file_path):
    """Load a user profile from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading profile from {file_path}: {str(e)}")
        return None

def save_sample_profile(output_file):
    """Save a sample profile to a JSON file for reference"""
    sample_profile = {
        "Full Name": "John Smith",
        "Age": 35,
        "Gender": "Male",
        "Height": "180 cm",
        "Weight": "85 kg",
        "Health Concerns": "High stress levels, occasional back pain",
        "Dietary Restrictions": "Lactose intolerant",
        "Exercise Frequency": "2-3 times per week",
        "Goals": "Reduce stress, lose 5kg, improve overall fitness",
        "Occupation": "Software Engineer (sedentary)",
        "Sleep Duration": "6-7 hours per night",
        "Water Intake": "approximately 1.5 liters daily"
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_profile, f, indent=4)
        print(f"Sample profile saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving sample profile: {str(e)}")
        return False

def create_profile_interactively():
    """Create a user profile through interactive prompts"""
    profile = {}
    
    print("\n=== Create User Profile ===\n")
    
    # Required fields
    profile["Full Name"] = input("Full Name: ")
    
    try:
        profile["Age"] = int(input("Age: "))
    except ValueError:
        profile["Age"] = input("Age (as text): ")
    
    profile["Gender"] = input("Gender: ")
    profile["Height"] = input("Height (e.g., 180 cm): ")
    profile["Weight"] = input("Weight (e.g., 85 kg): ")
    
    # Optional fields
    profile["Health Concerns"] = input("Health Concerns (or press Enter to skip): ")
    profile["Dietary Restrictions"] = input("Dietary Restrictions (or press Enter to skip): ")
    profile["Exercise Frequency"] = input("Exercise Frequency (or press Enter to skip): ")
    profile["Goals"] = input("Health/Fitness Goals (or press Enter to skip): ")
    
    # Remove empty fields
    profile = {k: v for k, v in profile.items() if v}
    
    return profile

def generate_plan_for_profile(profile, output_dir="generated_plans"):
    """Generate a wellness plan for the given profile"""
    if not profile:
        print("Error: No profile provided")
        return False
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate unique filename based on user name and timestamp
    user_name = profile.get("Full Name", "anonymous").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"wellness_plan_{user_name}_{timestamp}.md")
    
    # Generate the plan
    print(f"\nGenerating wellness plan for {profile.get('Full Name', 'user')}...")
    wellness_plan = ci.generate_wellness_plan(profile)
    
    if wellness_plan:
        # Save the plan to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(wellness_plan)
        print(f"Wellness plan generated successfully and saved to {output_file}")
        return output_file
    else:
        print("Failed to generate wellness plan")
        return False

def ensure_api_key():
    """Make sure we have an API key available"""
    # If the imported module doesn't have a key, try to set it
    if not ci.COHERE_API_KEY:
        # Try to use the fallback key
        manual_test_key = "q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh"
        print(f"Setting API key from test_cohere_wellness.py...")
        if hasattr(ci, 'set_test_api_key'):
            ci.set_test_api_key(manual_test_key)
            return True
        else:
            print("ERROR: Could not set API key. Missing set_test_api_key function.")
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate wellness plans using Cohere API')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--profile', type=str, help='Path to JSON file containing user profile')
    group.add_argument('--interactive', action='store_true', help='Create profile interactively')
    group.add_argument('--sample', type=str, help='Save a sample profile to the specified JSON file')
    args = parser.parse_args()
    
    # For sample profile generation, we don't need the API key
    if args.sample:
        save_sample_profile(args.sample)
        return
    
    # Ensure we have an API key for other operations
    if not ensure_api_key():
        print("WARNING: Unable to obtain a valid Cohere API key.")
        print("Limited functionality available.")
    
    # Handle different modes
    if args.profile:
        profile = load_profile_from_file(args.profile)
        if profile:
            generate_plan_for_profile(profile)
    elif args.interactive:
        profile = create_profile_interactively()
        generate_plan_for_profile(profile)
    else:
        # Default: run the tests
        print("No mode specified. Running tests...")
        if hasattr(ci, 'run_tests'):
            ci.run_tests()
        else:
            print("ERROR: run_tests function not found in cohere_integration module.")

if __name__ == "__main__":
    main() 
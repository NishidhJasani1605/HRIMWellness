import cohere
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Use API key from environment variable
COHERE_API_KEY = os.getenv('q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh')

# Check if API key is available
if not COHERE_API_KEY:
    print("WARNING: COHERE_API_KEY not found in environment variables.")
    print("Please check your .env file or set the environment variable.")
    print("Using default test mode with limited functionality.")
    # Initialize a dummy client that will be replaced if we set the API key later
    co = None
else:
    print(f"Using Cohere API Key: {COHERE_API_KEY[:5]}...{COHERE_API_KEY[-5:]}")
    # Initialize Cohere client
    co = cohere.Client(COHERE_API_KEY)

def generate_wellness_plan(user_profile):
    """
    Generate a personalized wellness plan using the Cohere API
    
    Args:
        user_profile (dict): User information including health data and preferences
        
    Returns:
        str: Generated wellness plan in Markdown format
    """
    if not co:
        print("ERROR: Cannot generate wellness plan without valid API key")
        return None
        
    # Convert user profile to a formatted string
    profile_str = format_user_profile(user_profile)
    
    # Create the prompt for Cohere
    prompt = f"""
    You are a certified wellness expert and dietician. Create a personalized wellness and diet plan for a client with the following profile:
    
    {profile_str}
    
    The wellness plan should include:
    1. A brief introduction addressing the client by name
    2. Diet recommendations based on their preferences and health needs
    3. Exercise recommendations considering their current activity level
    4. Lifestyle modifications that would benefit their specific situation
    5. A sample 3-day meal plan
    6. A weekly exercise schedule
    
    Format the response in Markdown with appropriate headings and bullet points.
    """
    
    try:
        # Generate response using Cohere
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        
        # Extract the generated text
        wellness_plan = response.generations[0].text
        print(f"Successfully generated wellness plan ({len(wellness_plan)} characters)")
        
        return wellness_plan
    
    except Exception as e:
        print(f"Error generating wellness plan: {str(e)}")
        return None

def format_user_profile(user_profile):
    """Format user profile into a readable string"""
    formatted = []
    
    # Add important fields first
    priority_fields = ['Full Name', 'Age', 'Gender', 'Height', 'Weight', 'Health Concerns', 
                       'Dietary Restrictions', 'Exercise Frequency', 'Goals']
    
    for field in priority_fields:
        if field in user_profile:
            formatted.append(f"{field}: {user_profile[field]}")
    
    # Add remaining fields
    for key, value in user_profile.items():
        if key not in priority_fields:
            formatted.append(f"{key}: {value}")
    
    return "\n".join(formatted)

def get_text_files_path():
    """
    Returns the path to the text_files directory
    Checks both the app/data/text_files and root text_files locations
    """
    # Option 1: App structure path
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'text_files')
    
    # Option 2: Root path
    root_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'text_files')
    
    # Check which one exists and return it
    if os.path.exists(root_path):
        return root_path
    else:
        return app_path

def get_sample_wellness_plan_path():
    """Returns the path to the sample_wellness_plan.md file"""
    return os.path.join(get_text_files_path(), 'sample_wellness_plan.md')

def create_test_profile():
    """Create a test profile for generation testing"""
    return {
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

def test_generation():
    """Test generating a wellness plan"""
    print("Testing wellness plan generation...")
    
    # Create a test profile
    test_profile = create_test_profile()
    
    # Generate the wellness plan
    wellness_plan = generate_wellness_plan(test_profile)
    
    if wellness_plan:
        # Save to a file for review
        sample_plan_path = get_sample_wellness_plan_path()
        with open(sample_plan_path, "w", encoding="utf-8") as f:
            f.write(wellness_plan)
        print(f"Sample wellness plan saved to '{sample_plan_path}'")
        return True
    else:
        print("Failed to generate wellness plan")
        return False

def test_cohere_api():
    """Test basic functionality of the Cohere API"""
    if not co:
        print("ERROR: Cannot test API without valid API key")
        return False
        
    try:
        print("\n=== Testing Cohere API Connection ===")
        # Test a simple completion
        response = co.generate(
            model='command',
            prompt='Write a short haiku about wellness.',
            max_tokens=50,
            temperature=0.7
        )
        
        print("API Response:")
        print(response.generations[0].text)
        print("\nAPI is working correctly!")
        return True
    except Exception as e:
        print(f"Error testing Cohere API: {str(e)}")
        return False

def test_api_key_setup():
    """Test if the API key is correctly set up"""
    print("\n=== Testing API Key Configuration ===")
    
    if not COHERE_API_KEY:
        print("❌ FAIL: API key not found in environment variables")
        
        # Try to read directly from .env file
        try:
            with open('.env', 'r') as f:
                env_contents = f.read()
                if 'COHERE_API_KEY' in env_contents:
                    print("✓ .env file contains COHERE_API_KEY entry")
                    print("  But dotenv failed to load it correctly")
                else:
                    print("❌ .env file doesn't contain COHERE_API_KEY entry")
        except Exception as e:
            print(f"❌ Error reading .env file: {str(e)}")
            
        return False
    else:
        print(f"✅ PASS: API key found: {COHERE_API_KEY[:5]}...{COHERE_API_KEY[-5:]}")
        return True

def run_tests():
    """Run all tests for the Cohere integration"""
    print("\n===== COHERE API INTEGRATION TESTS =====\n")
    
    # Test API key setup
    api_key_ok = test_api_key_setup()
    
    if api_key_ok:
        # Test the API connection
        api_works = test_cohere_api()
        
        if api_works:
            # Test the wellness plan generation
            print("\n=== Testing Wellness Plan Generation ===")
            generation_works = test_generation()
        else:
            print("\nSkipping wellness plan test due to API connection failure.")
            generation_works = False
    else:
        print("\nSkipping API tests due to missing API key.")
        api_works = False
        generation_works = False
    
    print("\n===== TEST SUMMARY =====")
    print(f"API Key Configuration: {'✅ PASS' if api_key_ok else '❌ FAIL'}")
    print(f"API Connection: {'✅ PASS' if api_works else '❌ FAIL'}")
    
    # Check if the wellness plan was generated
    sample_plan_path = get_sample_wellness_plan_path()
    wellness_plan_exists = os.path.exists(sample_plan_path)
    print(f"Wellness Plan Generation: {'✅ PASS' if generation_works and wellness_plan_exists else '❌ FAIL'}")
    
    if wellness_plan_exists:
        # Get file size
        file_size = os.path.getsize(sample_plan_path) / 1024  # KB
        print(f"Generated Plan Size: {file_size:.2f} KB")
    
    print("\n===== END OF TESTS =====")
    
    return all([api_key_ok, api_works, generation_works])

def set_test_api_key(key):
    """Set API key for testing purposes (used when no env variable is found)"""
    global COHERE_API_KEY, co
    
    COHERE_API_KEY = key
    print(f"Setting test API key: {COHERE_API_KEY[:5]}...{COHERE_API_KEY[-5:]}")
    co = cohere.Client(COHERE_API_KEY)
    return True

if __name__ == "__main__":
    # Run all tests
    manual_test_key = "q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh"  # As a fallback
    
    if not COHERE_API_KEY and manual_test_key:
        print("\n=== No API key found in environment, using manual test key ===")
        set_test_api_key(manual_test_key)
    
    success = run_tests()
    
    # Exit with appropriate status code
    if not success:
        print("\nSome tests failed. Please check the output above for details.")
        exit(1) 
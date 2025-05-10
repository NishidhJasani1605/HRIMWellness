# Cohere API Integration for HRIM Wellness

This module provides integration with the Cohere API for generating personalized wellness and diet plans.

## Features

- Generate personalized wellness plans based on user profiles
- Test the Cohere API connection
- Create user profiles interactively or via JSON files
- Output wellness plans as Markdown files

## Setup

1. **Install Required Packages**:

   ```bash
   pip install cohere python-dotenv
   ```

2. **Set up API Key**:

   Add your Cohere API key to the `.env` file:

   ```
   COHERE_API_KEY=your_api_key_here
   ```

## Usage

### Basic Testing

Run the test script to verify the API connection and wellness plan generation:

```bash
python cohere_integration.py
```

### Generate Wellness Plans with Custom Profiles

Use the `test_cohere_wellness.py` script to generate plans with different options:

1. **Create a profile interactively**:

   ```bash
   python test_cohere_wellness.py --interactive
   ```

2. **Use a JSON profile file**:

   ```bash
   python test_cohere_wellness.py --profile path/to/profile.json
   ```

3. **Save a sample profile**:

   ```bash
   python test_cohere_wellness.py --sample sample_profile.json
   ```

### Sample Profile Format

```json
{
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
```

## Integration with HRIM Wellness

To integrate this module with the main HRIM Wellness system:

### In `automate_workflow.py`:

```python
import cohere_integration as ci

# When generating a wellness plan for a user:
user_profile = {
    "Full Name": form_data.get("name"),
    "Age": form_data.get("age"),
    # ... other profile data
}

wellness_plan = ci.generate_wellness_plan(user_profile)

# Then use this wellness plan with your PDF generation code
```

### In `whatsapp_chatbot.py`:

```python
import cohere_integration as ci

# When a user requests a quick tip or advice:
response = ci.co.generate(
    model='command',
    prompt=f'Provide a quick wellness tip for someone who is {user_concern}',
    max_tokens=150,
    temperature=0.7
)
```

## Output

The generated wellness plans include:

1. A personalized introduction
2. Diet recommendations
3. Exercise recommendations
4. Lifestyle modifications
5. A sample 3-day meal plan
6. A weekly exercise schedule

All plans are formatted in Markdown and saved to the `generated_plans` directory.

## Troubleshooting

If you encounter any issues:

1. Verify your API key is correctly set in the `.env` file
2. Check your internet connection
3. Run the test script to diagnose API connection issues:
   ```bash
   python cohere_integration.py
   ```
4. Review the API response for any error messages

## API Documentation

For more information about the Cohere API, visit:
https://docs.cohere.com/ 
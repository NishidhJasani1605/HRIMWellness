#!/usr/bin/env python3
"""
Test script to generate a wellness PDF with improved header and content layout.
This script will use a sample wellness plan and generate a PDF to test the layout fixes.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add the project root to the path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from app.core.wellness.generate_wellness_pdf import create_pdf, process_form_data
except ImportError:
    print("Error: Could not import wellness PDF generation modules.")
    print("Make sure you are running this script from the project root directory.")
    sys.exit(1)

def load_sample_data():
    """Load sample user data from the sample form data file"""
    try:
        with open('sample_form_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create basic sample data if file doesn't exist
        return {
            "Full Name": "Test User",
            "Age": 35,
            "Gender": "Female",
            "Height": 165,
            "Weight": 68,
            "Email": "test@example.com",
            "Phone": "+91 98765 43210",
            "Primary Health Goal": "Weight loss",
            "Dietary Preference": "Vegetarian",
            "Activity Level": "Sedentary",
            "Stress Level": "Moderate",
            "Water Intake": "1.5 liters/day",
            "Sleep": "6 hours",
            "Allergies": "None reported",
        }

def generate_sample_wellness_plan(user_data):
    """Generate a simplified wellness plan for testing purposes"""
    name = user_data.get('Full Name', 'Client')
    
    md_content = f"""# Diet & Wellness Plan

## Client Summary

* Name: {name}
* Age: {user_data.get('Age', 30)} (Born: {datetime.now().year - int(user_data.get('Age', 30))})
* Gender: {user_data.get('Gender', 'Not specified')}
* Occupation: {user_data.get('Occupation', 'Not specified')}
* Height: {user_data.get('Height', 165)} cm
* Weight: {user_data.get('Weight', 70)} kg

## Health Concerns

* Primary Health Goal: {user_data.get('Primary Health Goal', 'Weight loss')}
* Current Symptoms/Diagnosis: {user_data.get('Medical Conditions', 'No existing medical conditions reported')}
* Medications: {user_data.get('Medications', 'None')}
* Stress Levels: {user_data.get('Stress Level', 'Moderate')}
* Allergies: {user_data.get('Allergies', 'None reported')}

## Dietary Habits

* Dietary Preference: {user_data.get('Dietary Preference', 'Vegetarian')}
* Meals Per Day: 3
* Snacking Habit: Occasional
* Water Intake: {user_data.get('Water Intake', '1.5 liters/day')}
* Caffeine Intake: 2 cups/day (tea/coffee)
* Frequency of Eating Out: Rarely

## Activity & Lifestyle

* Physical Activity: {user_data.get('Activity Level', 'Sedentary')}
* Sleep: {user_data.get('Sleep', '6 hours')} (Wake-up: 06:00, Sleep: 23:30)
* Screen Time: 3 hours/day
* Hobbies: Traveling

## Other Inputs

* Wellness Goals: Weight loss
* Emotional State: Sometimes stressed
* Relaxation Techniques: None reported
* Menstrual Health: Not specified (assumed regular based on age)
* Cravings: Not specified

## Nutritional Goals

* Calorie Target: ~1500-1600 kcal/day (to support gradual weight loss of ~0.5 kg/week)
* Macronutrient Breakdown:
  * Protein: 20% (~75-80 g)
  * Fat: 25% (~40-45 g)
  * Carbohydrates: 55% (~200-220 g)
  * Fiber: 25-30 g/day
* Focus: High-fiber, moderate protein vegetarian meals using Gujarat-specific ingredients, promoting satiety and mindful eating (75% full).

## 7-Day Diet & Wellness Plan

### Notes

* Meals: Quick to prepare (<30 minutes), using Gujarat specific vegetables (e.g., valor, tindora), fruits (e.g., chikoo, guava), spices (e.g., cumin, turmeric), and grains (e.g., bajra, jowar).
* Portions: Designed for mindful eating (stop at 75% full).
* Hydration: Aim for 2.5-3 liters water/day.
* State Context: Gujarat-based, accessible in Surat markets.

## Day 1: Monday

### Meal Plan

* Breakfast (7:00 AM): Poha with Vegetables
  * Ingredients (1 serving): Flattened rice (50g), onion (30g), green peas (20g), mustard seeds (1g), turmeric (1g), green chili (1g), lemon juice (5ml), coriander leaves (5g), oil (5ml).
  * Recipe: Rinse poha, soak briefly. Heat oil, add mustard seeds, turmeric, chili, onion, peas. Add poha, cook 5 min. Garnish with lemon, coriander.
  * Calories: 250 kcal | Protein: 5g | Fat: 7g | Carbs: 42g | Fiber: 3g

* Lunch (1:00 PM): Gujarati Dal, Bhindi Sabzi, Roti, Curd
  * Ingredients (1 serving): Toor dal (40g), bhindi (100g), whole wheat flour (50g), curd (100g), cumin (1g), turmeric (1g), garam masala (1g), oil (5ml), ginger (2g), garlic (1g).
  * Recipe: Cook dal with turmeric, tomato, ginger. Temper with cumin. Sauté bhindi with spices. Make 2 rotis. Serve with curd.
  * Calories: 550 kcal | Protein: 20g | Fat: 15g | Carbs: 85g | Fiber: 12g

* Dinner (7:30 PM): Vegetable Khichdi, Cucumber Raita
  * Ingredients (1 serving): Rice (50g), moong dal (20g), carrot (20g), beans (30g), cumin (1g), turmeric (1g), curd (50g), cucumber (50g), oil (5ml).
  * Recipe: Cook rice, dal, vegetables with spices. Blend curd with grated cucumber for raita.
  * Calories: 400 kcal | Protein: 15g | Fat: 10g | Carbs: 65g | Fiber: 8g

* Total: ~1200 kcal | Protein: 40g | Fat: 32g | Carbs: 192g | Fiber: 23g

### Wellness & Activity Plan

* Morning (6:15 AM):
  * Pranayama: Anulom Vilom (5 min) - Alternate nostril breathing to reduce stress.
  * Yoga: Surya Namaskar (3 rounds, 10 min) - Full-body stretch.
* Evening (6:00 PM):
  * Exercise: Brisk walk (20 min, ~2 km) to improve stamina.
  * Meditation: Guided body scan (5 min) for mindfulness.
* Wellness Reminders:
  * Drink 500ml water upon waking.
  * Limit screen time to 2 hours (avoid 1 hour before bed).
  * Sleep by 22:30 for 7-8 hours.
  * Practice mindful eating: Chew slowly, savor flavors.

## Day 2: Tuesday

### Meal Plan

* Breakfast: Vegetable Upma
  * Ingredients: Sooji (50g), beans (20g), carrot (20g), mustard seeds (1g), curry leaves (2g), oil (5ml), green chili (1g).
  * Recipe: Roast sooji. Sauté mustard, curry leaves, chili, vegetables. Add water, sooji, cook until thick.
  * Calories: 260 kcal | Protein: 6g | Fat: 8g | Carbs: 40g | Fiber: 4g

* Lunch: Chole, Valor Sabzi, Roti
  * Ingredients: Chickpeas (50g), valor (100g), whole wheat flour (50g), onion (30g), tomato (30g), chana masala (2g), oil (5ml).
  * Recipe: Cook chickpeas with spices. Sauté valor with onion, tomato. Make 2 rotis.
  * Calories: 570 kcal | Protein: 22g | Fat: 16g | Carbs: 85g | Fiber: 14g

* Dinner: Methi Thepla, Tomato Sabzi
  * Ingredients: Whole wheat flour (50g), methi leaves (30g), tomato (100g), ajwain (1g), turmeric (1g), oil (5ml).
  * Recipe: Knead dough with methi, spices. Make 2 theplas. Cook tomato with spices.
  * Calories: 380 kcal | Protein: 12g | Fat: 12g | Carbs: 58g | Fiber: 10g

* Total: ~1210 kcal | Protein: 40g | Fat: 36g | Carbs: 183g | Fiber: 28g

### Wellness & Activity Plan

* Morning:
  * Pranayama: Kapalbhati (3 min) - Boosts metabolism.
  * Yoga: Tadasana, Vrikshasana (10 min) - Improves balance.
* Evening:
  * Exercise: Bodyweight squats (3 sets of 10, 10 min).
  * Meditation: Gratitude journaling (5 min).
* Wellness Reminders: Same as Day 1.
"""

    return md_content

def main():
    """Main function to run the test"""
    # Create output directory if it doesn't exist
    output_dir = Path('generated_data')
    output_dir.mkdir(exist_ok=True)
    
    # Load sample user data
    sample_data = load_sample_data()
    
    # Generate sample wellness plan
    wellness_plan = generate_sample_wellness_plan(sample_data)
    
    # Generate the PDF
    output_file = f"test_wellness_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = create_pdf(wellness_plan, sample_data, output_file)
    
    if pdf_path:
        print(f"Success! PDF generated at: {pdf_path}")
        print("Please check that the header is not overlapping with content and the structure is consistent.")
    else:
        print("Error generating PDF.")

if __name__ == "__main__":
    print("=== Testing HRIM Wellness PDF Layout ===")
    main() 
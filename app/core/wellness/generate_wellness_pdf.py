import os
import json
from datetime import datetime
import markdown
from app.api import cohere_integration as ci
from dotenv import load_dotenv

# Try to import WeasyPrint, but provide fallback
try:
    from weasyprint import HTML, CSS
    from weasyprint import default_url_fetcher
    WEASYPRINT_AVAILABLE = True
    print("WeasyPrint successfully imported.")
except Exception as e:
    print(f"Error importing WeasyPrint: {str(e)}")
    print("PDF generation will be disabled.")
    WEASYPRINT_AVAILABLE = False

# Load environment variables
load_dotenv()

def map_form_data_to_profile(form_data):
    """Map the form data to a user profile for Cohere API"""
    profile = {
        "Full Name": form_data.get("Full Name", ""),
        "Age": calculate_age(form_data.get("Date of Birth", "")),
        "Gender": form_data.get("Gender", ""),
        "Height": f"{form_data.get('Height (in cm)', '')} cm",
        "Weight": f"{form_data.get('Current Weight (in kg)', '')} kg",
        "Target Weight": form_data.get("Target Weight (if any)", ""),
        "Health Goals": form_data.get("Primary Health Goals", ""),
        "Health Concerns": form_data.get("If yes, please specify medical conditions", ""),
        "Medications": "Yes" if form_data.get("Are you currently on any medication?", "No") == "Yes" else "No",
        "Allergies": form_data.get("If yes, please specify allergies", ""),
        "Family Medical History": form_data.get("Family Medical History", ""),
        "Wake-Up Time": form_data.get("Wake-Up Time", ""),
        "Sleep Time": form_data.get("Sleep Time", ""),
        "Average Hours of Sleep": form_data.get("Average Hours of Sleep", ""),
        "Work Schedule": form_data.get("Work Schedule", ""),
        "Physical Activity Level": form_data.get("Physical Activity Level", ""),
        "Exercise Routine": form_data.get("Exercise Routine (if any)", ""),
        "Stress Levels": form_data.get("Stress Levels", ""),
        "Screen Time": f"{form_data.get('Screen Time per Day (Hours)', '')} hours",
        "Dietary Preference": form_data.get("Dietary Preference", ""),
        "Dietary Restrictions": form_data.get("If yes, please specify Dietary Restrictions", ""),
        "Meals Per Day": form_data.get("Meals Per Day", ""),
        "Snacking Habit": form_data.get("Snacking Habit", ""),
        "Water Intake": f"{form_data.get('Water Intake Per Day (in Liters)', '')} liters",
        "Caffeine Consumption": f"{form_data.get('Consumption of Caffeine (Tea/Coffee) Cups Per Day', '')} cups",
        "Eating Out Frequency": form_data.get("Frequency of Eating Out", ""),
        "Stress Frequency": form_data.get("How often do you feel stressed?", ""),
        "Relaxation Techniques": form_data.get("If yes, specify relaxation techniques", ""),
        "Hobbies": form_data.get("Hobbies and Leisure Activities (Describe)", ""),
        "Specific Concerns": form_data.get("Any specific concerns or goals you would like to address?", ""),
        "Previous Diet Plans": form_data.get("If yes, what type and what were the results?", ""),
        "Occupation": form_data.get("Occupation", ""),
        "City": form_data.get("City", ""),
        "State": form_data.get("State", ""),
        "Country": form_data.get("Country", ""),
        "Marital Status": form_data.get("Marital Status", "")
    }
    
    # Remove empty fields
    return {k: v for k, v in profile.items() if v}

def calculate_age(dob_str):
    """Calculate age from date of birth string"""
    if not dob_str:
        return ""
    
    try:
        # Assuming dob_str is in format YYYY-MM-DD
        dob_date = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return str(age)
    except Exception as e:
        print(f"Error calculating age: {e}")
        return ""

def generate_prompt_from_profile(profile):
    """Generate a custom prompt for the Cohere API based on user profile"""
    
    # Create a detailed prompt that incorporates all the user's information
    prompt = f"""
    Create a customized Diet & Wellness Plan for {profile.get('Full Name', 'the client')}, designed to address their specific health needs, goals, and lifestyle habits. The plan should be in markdown format, structured like a professional wellness report.
    
    CLIENT INFORMATION:
    - Name: {profile.get('Full Name', '')}
    - Age: {profile.get('Age', '')}
    - Gender: {profile.get('Gender', '')}
    - Height: {profile.get('Height', '')}
    - Weight: {profile.get('Weight', '')}
    - Target Weight: {profile.get('Target Weight', 'Not specified')}
    - Health Goals: {profile.get('Health Goals', 'Not specified')}
    - Occupation: {profile.get('Occupation', 'Not specified')}
    - City/State: {profile.get('City', '')}, {profile.get('State', '')}
    - Marital Status: {profile.get('Marital Status', '')}
    
    HEALTH INFORMATION:
    - Health Concerns: {profile.get('Health Concerns', 'None mentioned')}
    - Current Medications: {profile.get('Medications', 'None')}
    - Allergies: {profile.get('Allergies', 'None mentioned')}
    - Family Medical History: {profile.get('Family Medical History', 'Not provided')}
    
    LIFESTYLE INFORMATION:
    - Wake-Up Time: {profile.get('Wake-Up Time', '')}
    - Sleep Time: {profile.get('Sleep Time', '')}
    - Average Sleep: {profile.get('Average Hours of Sleep', '')}
    - Work Schedule: {profile.get('Work Schedule', '')}
    - Physical Activity: {profile.get('Physical Activity Level', '')}
    - Exercise Routine: {profile.get('Exercise Routine', 'None specified')}
    - Stress Levels: {profile.get('Stress Levels', '')}
    - Screen Time: {profile.get('Screen Time', '')}
    
    DIETARY INFORMATION:
    - Dietary Preference: {profile.get('Dietary Preference', '')}
    - Dietary Restrictions: {profile.get('Dietary Restrictions', 'None mentioned')}
    - Meals Per Day: {profile.get('Meals Per Day', '')}
    - Snacking Habits: {profile.get('Snacking Habit', '')}
    - Water Intake: {profile.get('Water Intake', '')}
    - Caffeine Consumption: {profile.get('Caffeine Consumption', '')}
    - Eating Out Frequency: {profile.get('Eating Out Frequency', '')}
    
    MENTAL WELLBEING:
    - Stress Frequency: {profile.get('Stress Frequency', '')}
    - Relaxation Techniques: {profile.get('Relaxation Techniques', 'None mentioned')}
    - Hobbies: {profile.get('Hobbies', 'Not specified')}
    
    ADDITIONAL INFORMATION:
    - Specific Concerns: {profile.get('Specific Concerns', 'None mentioned')}
    - Previous Diet Plans: {profile.get('Previous Diet Plans', 'None mentioned')}
    
    Based on this information, please create a 7-day wellness plan with the following sections:
    
    1. **Client Summary:**
       - Include key client details: Name, Age, Gender, Occupation, Height, Weight, Goals, etc.
       
    2. **Health Concerns:**
       - Note specific health issues and medications
       - Primary health goals
       - Any allergies or dietary restrictions
       
    3. **Nutritional Goals:**
       - Calorie targets and macronutrient breakdown (protein, fat, carbs, fiber)
       - Focus areas for diet improvement
       
    4. **Day-wise Meal Plan (7 days):**
       - Create a 7-day meal plan with breakfast, lunch, and dinner
       - For each meal, include ingredients (with quantities), recipe steps, and calorie/macronutrient content
       - Include notes about preparation time and hydration recommendations
       - Use locally available ingredients appropriate for Gujarat/India
       
    5. **Wellness & Activity Plan:**
       - Daily exercise and mindfulness practices
       - Morning and evening routines
       - Screen time management suggestions
       
    6. **Grocery List:**
       - Categorize items: Vegetables, Fruits, Grains & Cereals, Pulses, Spices, Dry Fruits, Others
       - Include quantities needed for the meal plan
       
    7. **Do's and Don'ts:**
       - List 4-5 specific behaviors to follow
       - List 4-5 specific behaviors to avoid
       
    8. **Summary Advice for Follow-Up:**
       - Progress monitoring suggestions
       - When to revisit the plan
       - Contact information for follow-up
       
    IMPORTANT FORMAT INSTRUCTIONS:
    - Use proper markdown heading levels: # for main sections, ## for subsections
    - Use bullet points for lists
    - For meal plans, use a clear structure with headings for each day and meal
    - Include horizontal dividers (---) between major sections
    - Avoid using non-standard markdown syntax
    - Format the entire output as clean, properly indented markdown
    - Make every heading clear and descriptive
    - Format all quantities in standard units (g, kg, ml, cups, etc.)
    - For recipes, clearly separate ingredients from instructions
    - Ensure all bullet points are properly indented
    """
    
    return prompt

def generate_wellness_plan_custom(profile):
    """Generate a wellness plan using the Cohere API with a custom prompt"""
    prompt = generate_prompt_from_profile(profile)
    
    try:
        # Generate response using Cohere
        response = ci.co.generate(
            model='command',
            prompt=prompt,
            max_tokens=3000,  # Increased token limit for longer response
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

def save_markdown_file(content, user_profile, output_dir=None):
    """Save markdown content to a file"""
    try:
        # Determine output directory
        if output_dir is None:
            output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        user_name = user_profile.get('Full Name', 'anonymous').replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
        output_path = os.path.join(output_dir, output_filename)
        
        # Write content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Markdown file saved successfully: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error saving markdown file: {str(e)}")
        return None

def create_pdf(wellness_plan, user_profile, output_filename=None):
    """
    Convert wellness plan to PDF
    
    Args:
        wellness_plan: Wellness plan in markdown format
        user_profile: User information dictionary
        output_filename: Name for the output file (optional)
        
    Returns:
        Path to the generated PDF
    """
    if not WEASYPRINT_AVAILABLE:
        print("WeasyPrint not available. Saving as markdown only.")
        return save_markdown_file(wellness_plan, user_profile)
    
    try:
        # Generate output filename if not provided
        if not output_filename:
            user_name = user_profile.get('Full Name', 'anonymous').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"wellness_plan_{user_name}_{timestamp}.pdf"
        
        # Ensure output directory exists
        output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        
        # Preprocess the markdown content to ensure proper formatting
        wellness_plan = wellness_plan.strip()
        
        # Pre-process markdown to get cleaner formatting
        # Fix any common markdown formatting issues and restructure for better document appearance
        import re
        lines = wellness_plan.split('\n')
        
        # Track section structure for better page breaks
        new_lines = []
        in_list = False
        day_section = False
        
        for i in range(len(lines)):
            line = lines[i]
            
            # Fix headings format
            if line.startswith('#'):
                if day_section:
                    # Close any previous day section
                    day_section = False
                
                # Fix hashtag headings that don't have a space after the hashtag
                count = 0
                for char in line:
                    if char == '#':
                        count += 1
                    else:
                        break
                if count > 0 and count <= 6:  # Valid heading levels
                    if line[count:count+1] != ' ':
                        line = line[:count] + ' ' + line[count:]
                        
                # Add an empty line before headings unless it's already there
                if i > 0 and new_lines and new_lines[-1].strip() != '':
                    new_lines.append('')
                    
                # Add special class for day sections for better page breaks and styling
                if line.lower().startswith('## day'):
                    line = f'<div class="day-section">{line}'
                    day_section = True
                # Add special class for meal plans
                elif 'meal plan' in line.lower() and count == 3:  # Level 3 heading with "meal plan"
                    line = f'<div class="meal-section">{line}'
                # Add special class for grocery lists
                elif 'grocery list' in line.lower() and count <= 2:
                    line = f'<div class="grocery-list">{line}'
                    
            # Handle list items to ensure proper document structure
            if (line.strip().startswith('- ') or line.strip().startswith('* ')) and not in_list:
                in_list = True
            elif in_list and not (line.strip().startswith('- ') or line.strip().startswith('* ')) and line.strip() != '':
                in_list = False
                
                # Close any open sections if we're at the end of a list
                if day_section and i < len(lines) - 1 and lines[i+1].startswith('##'):
                    new_lines.append('</div><!-- end day-section -->')
                    day_section = False
                    
            # Add the processed line
            new_lines.append(line)
            
            # Add empty line after headings for better spacing
            if line.startswith('#') and i < len(lines) - 1 and not lines[i+1].startswith('#'):
                if not 'grocery list' in line.lower():  # Don't add extra space before grocery lists
                    new_lines.append('')
            
        # Make sure any open sections are closed
        if day_section:
            new_lines.append('</div><!-- end day-section -->')
            
        # Add closing divs for any meal sections and grocery lists
        finalized_lines = []
        open_sections = []
        
        for line in new_lines:
            if '<div class="meal-section">' in line:
                open_sections.append('meal-section')
            elif '<div class="grocery-list">' in line:
                open_sections.append('grocery-list')
            elif '<div class="day-section">' in line:
                open_sections.append('day-section')
            elif line.startswith('##') and open_sections and open_sections[-1] in ['meal-section', 'grocery-list']:
                # Close before a new major section
                finalized_lines.append(f'</div><!-- end {open_sections.pop()} -->')
                
            finalized_lines.append(line)
            
        # Close any remaining open sections
        for section in reversed(open_sections):
            finalized_lines.append(f'</div><!-- end {section} -->')
                
        # Rejoin processed lines
        wellness_plan = '\n'.join(finalized_lines)
        
        # Convert markdown to HTML
        html_content = markdown_to_html(wellness_plan, user_profile)
        
        # Create a temporary file for HTML
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
            
        # Define additional CSS for page layout and pagination
        page_css = CSS(string="""
            @page {
                size: A4;
                margin: 160px 50px 80px 50px;
                @top-center {
                    content: element(header);
                }
                @bottom-center {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10pt;
                    color: #444;
                    margin-top: 0.5cm;
                }
            }
            
            /* Make header visible on all pages */
            .header {
                position: running(header);
                height: 160px;
                background: white;
                border-bottom: 1px solid #ccc;
                padding: 25px 40px 10px;
                box-sizing: border-box;
                text-align: center;
                width: 100%;
            }
            
            /* Make sure the content doesn't overlap with header */
            .content {
                margin-top: 10px;
                margin-bottom: 20mm;
            }
        """)
        
        # Generate PDF from HTML with better styling options
        HTML(filename=temp_html_path).write_pdf(
            output_path,
            presentational_hints=True,
            stylesheets=[page_css]
        )
        
        # Clean up temporary HTML file
        os.unlink(temp_html_path)
        
        print(f"PDF generated successfully: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        # Fallback to saving as markdown
        print("Falling back to saving as markdown.")
        return save_markdown_file(wellness_plan, user_profile)

def markdown_to_html(markdown_content, user_profile):
    """Convert markdown content to HTML with proper styling"""
    # Convert markdown to html using markdown library
    import markdown
    from datetime import datetime
    
    # Get user details
    user_name = user_profile.get('Full Name', 'Client')
    user_email = user_profile.get('Email', 'N/A')
    user_phone = user_profile.get('Phone', 'N/A')
    date_generated = datetime.now().strftime("%d %B, %Y")
    
    # Process markdown content before converting to improve structure
    # Add HTML classes to improve organization
    lines = markdown_content.split('\n')
    processed_lines = []
    
    in_meal_section = False
    in_day_section = False
    in_wellness_section = False
    
    for i, line in enumerate(lines):
        # Format day headings for better structure
        if line.strip().startswith('## Day'):
            if in_day_section:
                processed_lines.append('</div><!-- end day-section -->')
            processed_lines.append('<div class="day-section">')
            processed_lines.append(line)
            in_day_section = True
            continue
            
        # Format meal plan headings
        if 'Meal Plan' in line and line.startswith('#'):
            if in_meal_section:
                processed_lines.append('</div><!-- end meal-section -->')
            processed_lines.append('<div class="meal-section">')
            processed_lines.append(line)
            in_meal_section = True
            continue
            
        # Format wellness activity plan headings
        if 'Wellness' in line and 'Activity' in line and 'Plan' in line and line.startswith('#'):
            if in_wellness_section:
                processed_lines.append('</div><!-- end wellness-activity -->')
            processed_lines.append('<div class="wellness-activity">')
            processed_lines.append(line)
            in_wellness_section = True
            continue
            
        # Process meal items and format properly
        if in_meal_section and line.strip().startswith('* '):
            # Check if this is a meal time heading (Breakfast, Lunch, Dinner)
            meal_indicators = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
            is_meal_heading = any(indicator in line for indicator in meal_indicators)
            
            if is_meal_heading:
                # Add div for meal details
                processed_lines.append(line)
                processed_lines.append('<div class="meal-details">')
            else:
                # Add this line as meal detail
                processed_lines.append(line)
                
                # If next line doesn't start with *, close the meal details div
                if i + 1 >= len(lines) or not lines[i+1].strip().startswith('* '):
                    processed_lines.append('</div><!-- end meal-details -->')
            continue
        
        # Add the line normally if no special formatting needed
        processed_lines.append(line)
    
    # Close any open sections
    if in_meal_section:
        processed_lines.append('</div><!-- end meal-section -->')
    if in_wellness_section:
        processed_lines.append('</div><!-- end wellness-activity -->')
    if in_day_section:
        processed_lines.append('</div><!-- end day-section -->')
    
    # Rejoin the processed lines
    processed_markdown = '\n'.join(processed_lines)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(processed_markdown, extensions=['tables'])
    
    # Enhanced styles matching the client's desired format with improved document appearance
    styles = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Arial:wght@400;700&display=swap');
        
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #000;
            margin: 0;
            padding: 0;
            background-color: white;
            font-size: 12pt;
        }
        
        /* Header styling */
        .header {
            text-align: center;
            padding: 25px 40px 10px;
            background: white;
            border-bottom: 1px solid #ccc;
            width: 100%;
            box-sizing: border-box;
        }
        
        .header-section {
            text-align: center;
            font-weight: bold;
            font-size: 18pt;
            margin-bottom: 6px;
        }
        
        .subheading {
            text-align: center;
            font-size: 13pt;
            margin-bottom: 10px;
        }
        
        .address {
            text-align: center;
            font-size: 10pt;
            color: #333;
            line-height: 1.8;
        }
        
        /* Content styling */
        .content {
            margin: 20px;
            padding-top: 0;
        }
        
        /* Clean document style formatting */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Arial', sans-serif;
            page-break-after: avoid;
            color: #222;
        }
        
        h1 {
            font-size: 16pt;
            margin-top: 20px;
            margin-bottom: 10px;
            font-weight: bold;
            border-bottom: 1px solid #ccc;
            padding-bottom: 4px;
        }
        
        h2 {
            font-size: 14pt;
            margin-top: 20px;
            margin-bottom: 10px;
            font-weight: bold;
            page-break-before: auto; /* Allow appropriate page breaks */
        }
        
        h3 {
            font-size: 13pt;
            margin-top: 15px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        p {
            margin-bottom: 10px;
            margin-top: 0;
        }
        
        /* Fix list formatting to look more like a document */
        ul, ol {
            padding-left: 20px;
            margin-top: 5px;
            margin-bottom: 10px;
        }
        
        li {
            margin-bottom: 5px;
            line-height: 1.4;
        }
        
        /* Better spacing for sections */
        li p {
            margin: 3px 0;
        }
        
        /* Page break control */
        .day-section {
            page-break-before: auto;
            page-break-inside: avoid;
            margin-top: 20px;
        }
        
        /* Section formatting */
        .meal-section {
            margin-bottom: 15px;
            page-break-inside: avoid;
        }
        
        .meal-details {
            margin-left: 15px;
        }
        
        .grocery-list {
            page-break-inside: avoid;
        }
        
        /* Wellness activity plan formatting */
        .wellness-activity {
            page-break-inside: avoid;
        }
        
        /* Client details formatting */
        .client-details {
            margin: 10px 0;
        }
        
        .client-details p {
            margin: 6px 0;
            line-height: 1.4;
        }
        
        .client-details strong {
            display: inline-block;
            width: 120px;
            font-weight: bold;
        }
        
        /* Table formatting - only for grocery list */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 11pt;
        }
        
        th, td {
            border: 1px solid #ccc;
            padding: 6px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        /* Ensure proper spacing between sections */
        .section-divider {
            height: 1px;
            background-color: #eee;
            margin: 20px 0;
            width: 100%;
        }
        
        /* Calorie and nutritional info formatting */
        .nutritional-info {
            font-style: italic;
            color: #555;
            margin-top: 5px;
            margin-bottom: 10px;
        }
        
        /* Recipe formatting */
        .recipe {
            margin-left: 20px;
            margin-bottom: 15px;
        }
        
        /* Ingredients formatting */
        .ingredients {
            margin-left: 20px;
        }
        
        /* Bold labels */
        .label {
            font-weight: bold;
        }
        
        /* Day summary */
        .day-summary {
            border-top: 1px solid #eee;
            margin-top: 10px;
            padding-top: 5px;
            font-style: italic;
        }
        
        /* Links in header */
        .address a {
            color: #0000EE;
            text-decoration: none;
        }
    </style>
    """
    
    # Create HTML document with header and footer
    complete_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Diet & Wellness Plan - {user_name}</title>
        {styles}
    </head>
    <body>
        <div class="header">
            <div class="header-section">HRIM Wellness Centre</div>
            <div class="subheading">॥स्वस्थस्य स्वास्थ्य रक्षणम्॥</div>
            <div class="address">
                503, Takshshila Apartment, Dayalaji Ashram Marg, Majura Gate, Surat – 395001<br>
                📞 +91 94279 81235 &nbsp;|&nbsp; ✉️ <a href="mailto:hrimwellness@gmail.com">hrimwellness@gmail.com</a> &nbsp;|&nbsp; 🌐 <a href="http://www.hrimwellness.in">www.hrimwellness.in</a>
            </div>
        </div>
        
        <div class="content">
            {html_content}
        </div>
    </body>
    </html>
    """
    
    return complete_html

def process_form_data(form_data):
    """Process form data to generate a wellness plan PDF"""
    try:
        # Map form data to user profile
        user_profile = map_form_data_to_profile(form_data)
        
        # Generate wellness plan
        wellness_plan = generate_wellness_plan_custom(user_profile)
        
        if wellness_plan:
            # Create PDF if available, otherwise save as markdown
            if WEASYPRINT_AVAILABLE:
                return create_pdf(wellness_plan, user_profile)
            else:
                return save_markdown_file(wellness_plan, user_profile)
        else:
            print("Failed to generate wellness plan")
            return None
    
    except Exception as e:
        print(f"Error processing form data: {str(e)}")
        return None

def read_sample_form_data(file_path="sample_form_data.json"):
    """Read sample form data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading sample form data: {str(e)}")
        return None

def get_text_files_path():
    """
    Returns the path to the text_files directory
    Checks both the app/data/text_files and root text_files locations
    """
    # Option 1: App structure path
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'text_files')
    
    # Option 2: Root path
    root_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'text_files')
    
    # Check which one exists and return it
    if os.path.exists(root_path):
        return root_path
    else:
        return app_path

def get_form_structure_path():
    """Returns the path to the form_structure.txt file"""
    return os.path.join(get_text_files_path(), 'form_structure.txt')

def create_sample_form_data(file_path="sample_form_data.json"):
    """Create a sample form data file based on form_structure.txt"""
    # Comment: The form structure is now in the text_files directory
    sample_data = {
        "Email": "johndoe@example.com",
        "Full Name": "John Doe",
        "Date of Birth": "1985-05-15",
        "Gender": "Male",
        "WhatsApp Contact Number": "+91 9876543210",
        "Address": "123 Main Street",
        "City": "Surat",
        "PIN": "395001",
        "State": "Gujarat",
        "Country": "India",
        "Occupation": "Software Engineer",
        "Marital Status": "Married",
        "Height (in cm)": "175",
        "Current Weight (in kg)": "80",
        "Target Weight (if any)": "72",
        "Primary Health Goals": "Weight Loss, Stress Management",
        "Do you have any existing medical conditions?": "Yes",
        "If yes, please specify medical conditions": "Mild hypertension",
        "Are you currently on any medication?": "Yes",
        "Any allergies (food or otherwise)?": "No",
        "If yes, please specify allergies": "",
        "Family Medical History": "Diabetes, heart disease",
        "Wake-Up Time": "6:30 AM",
        "Sleep Time": "11:00 PM",
        "Average Hours of Sleep": "7.5",
        "Work Schedule": "Fixed",
        "Physical Activity Level": "Lightly Active",
        "Exercise Routine (if any)": "Walking for 20 minutes, 3 times a week",
        "Stress Levels": "Moderate",
        "Screen Time per Day (Hours)": "8",
        "Dietary Preference": "Vegetarian",
        "Any Dietary Restrictions?": "Yes",
        "If yes, please specify Dietary Restrictions": "No onions, no garlic",
        "Meals Per Day": "3",
        "Snacking Habit": "Occasionally",
        "Water Intake Per Day (in Liters)": "2",
        "Consumption of Caffeine (Tea/Coffee) Cups Per Day": "3",
        "Frequency of Eating Out": "Weekly",
        "How often do you feel stressed?": "Often",
        "Do you practice any relaxation techniques?": "Yes",
        "If yes, specify relaxation techniques": "Deep breathing",
        "Hobbies and Leisure Activities (Describe)": "Reading, gardening, watching movies",
        "Any specific concerns or goals you would like to address?": "Want to reduce belly fat and improve energy levels",
        "Have you followed any diet or fitness plan before?": "Yes",
        "If yes, what type and what were the results?": "Tried intermittent fasting for 2 months, lost 3kg but gained back"
    }
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=4)
        print(f"Sample form data created at {file_path}")
        return True
    except Exception as e:
        print(f"Error creating sample form data: {str(e)}")
        return False

def main():
    """Main function to test the wellness plan generation"""
    import argparse
    parser = argparse.ArgumentParser(description='Generate wellness plans from form data')
    parser.add_argument('--create-sample', action='store_true', help='Create a sample form data file')
    parser.add_argument('--form-data', type=str, help='Path to form data JSON file')
    args = parser.parse_args()
    
    print(f"Arguments: {args}")
    
    if args.create_sample:
        print("Creating sample form data...")
        result = create_sample_form_data()
        print(f"Result: {result}")
    elif args.form_data:
        print(f"Processing form data from {args.form_data}...")
        form_data = read_sample_form_data(args.form_data)
        if form_data:
            path = process_form_data(form_data)
            print(f"Generated wellness plan: {path}")
        else:
            print("Failed to read form data")
    else:
        print("No action specified. Use --create-sample to create sample data or --form-data to process a form data file.")
        print("Example: python generate_wellness_pdf.py --create-sample")
        print("Example: python generate_wellness_pdf.py --form-data sample_form_data.json")

if __name__ == "__main__":
    # Ensure the API key is set
    if not hasattr(ci, 'COHERE_API_KEY') or not ci.COHERE_API_KEY:
        test_key = "q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh"
        if hasattr(ci, 'set_test_api_key'):
            ci.set_test_api_key(test_key)
            print(f"Using test API key")
        else:
            print("Warning: No Cohere API key found and cannot set test key")
    
    main() 
import os
import sys
import argparse
import json
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from generate_test_wellness_plan.py
from tests.generate_test_wellness_plan import generate_random_form_data
from app.api.cohere_integration import generate_wellness_plan, set_test_api_key

# Import PDF generation modules
try:
    from app.core.wellness.generate_wellness_pdf import process_form_data, save_markdown_file, create_pdf
    PDF_AVAILABLE = True
except ImportError:
    print("Warning: PDF generation modules could not be imported.")
    PDF_AVAILABLE = False

def main():
    """Main function to run the wellness plan generator CLI"""
    # Set a test API key for Cohere
    test_api_key = "q9OWktdIYYibhnyQTp1hiAhNwUWg9pvrHI9moYlh"
    set_test_api_key(test_api_key)
    
    parser = argparse.ArgumentParser(description="HRIM Wellness Plan Generator")
    parser.add_argument("--random", action="store_true", help="Generate a plan with random data")
    parser.add_argument("--input", type=str, help="Path to JSON input file with form data")
    parser.add_argument("--output", type=str, help="Output directory for wellness plan (default: generated_data)")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF output (requires WeasyPrint)")
    parser.add_argument("--preview", action="store_true", help="Show a preview of the wellness plan")
    parser.add_argument("--save-form", type=str, help="Save generated form data to a JSON file")
    
    args = parser.parse_args()
    
    # Set output directory if specified
    if args.output:
        os.environ['GENERATED_DATA_PATH'] = args.output
        os.makedirs(args.output, exist_ok=True)
    
    # Generate form data
    form_data = None
    if args.random:
        print("Generating random form data...")
        form_data = generate_random_form_data()
        
        # Save form data if requested
        if args.save_form:
            with open(args.save_form, 'w', encoding='utf-8') as f:
                json.dump(form_data, f, indent=2)
            print(f"Random form data saved to: {args.save_form}")
    elif args.input:
        print(f"Loading form data from: {args.input}")
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                form_data = json.load(f)
        except Exception as e:
            print(f"Error loading form data: {str(e)}")
            return
    else:
        print("Either --random or --input must be specified")
        parser.print_help()
        return
    
    # Display form data summary
    print("\nForm Data Summary:")
    print(f"Name: {form_data.get('Full Name', 'Unknown')}")
    print(f"Age: {form_data.get('Age', calculate_age(form_data.get('Date of Birth', '')))}")
    print(f"Gender: {form_data.get('Gender', 'Unknown')}")
    print(f"Location: {form_data.get('City', '')}, {form_data.get('State', '')}")
    print(f"Health Goals: {form_data.get('Primary Health Goals', 'Unknown')}")
    print(f"Dietary Preference: {form_data.get('Dietary Preference', 'Unknown')}")
    
    # Generate wellness plan
    print("\nGenerating wellness plan...")
    
    # Generate wellness plan
    wellness_plan = generate_wellness_plan(form_data)
    if wellness_plan:
        if args.preview:
            preview_length = min(500, len(wellness_plan))
            print("\nWellness Plan Preview (first 500 characters):")
            print(wellness_plan[:preview_length] + "...\n")
        
        print(f"Total characters in wellness plan: {len(wellness_plan)}")
        
        # Process the wellness plan (PDF or markdown)
        if args.pdf and PDF_AVAILABLE:
            try:
                # Try to use the process_form_data function to generate PDF
                print("Generating PDF...")
                output_path = process_form_data(form_data)
                if output_path:
                    print(f"\nWellness plan saved to: {output_path}")
                else:
                    print("Failed to generate PDF, falling back to markdown")
                    # Save as markdown
                    user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
                    
                    output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
                    output_path = os.path.join(output_dir, output_filename)
                    
                    os.makedirs(output_dir, exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(wellness_plan)
                    
                    print(f"\nWellness plan saved to: {output_path}")
            except Exception as e:
                print(f"Error generating PDF: {e}")
                # Save as markdown if PDF generation fails
                user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
                
                output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
                output_path = os.path.join(output_dir, output_filename)
                
                os.makedirs(output_dir, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(wellness_plan)
                
                print(f"\nWellness plan saved to: {output_path}")
        elif args.pdf and not PDF_AVAILABLE:
            print("PDF generation is not available. Missing required modules. Generating markdown instead.")
            # Save as markdown
            user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
            
            output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
            output_path = os.path.join(output_dir, output_filename)
            
            os.makedirs(output_dir, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(wellness_plan)
            
            print(f"\nWellness plan saved to: {output_path}")
        else:
            # Save as markdown
            user_name = form_data.get('Full Name', 'anonymous').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"wellness_plan_{user_name}_{timestamp}.md"
            
            output_dir = os.environ.get('GENERATED_DATA_PATH', 'generated_data')
            output_path = os.path.join(output_dir, output_filename)
            
            os.makedirs(output_dir, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(wellness_plan)
            
            print(f"\nWellness plan saved to: {output_path}")
    else:
        print("Failed to generate wellness plan.")

def calculate_age(dob_str):
    """Calculate age from date of birth string"""
    if not dob_str:
        return "Unknown"
    
    try:
        # Assuming dob_str is in format YYYY-MM-DD
        dob_date = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return str(age)
    except Exception as e:
        print(f"Error calculating age: {e}")
        return "Unknown"

if __name__ == "__main__":
    print("=== HRIM Wellness Plan Generator CLI ===")
    main()
    print("\nDone!") 
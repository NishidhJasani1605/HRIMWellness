# HRIM Wellness Application

A comprehensive wellness plan generation application that creates personalized wellness plans for clients based on their health and lifestyle information.

## Project Structure

```
HRIMWellness/
├── app/
│   ├── api/                  # API integration (Cohere, LLM)
│   ├── core/                 # Core application functionality
│   │   └── wellness/         # Wellness plan generation
│   │       └── tests/        # Tests for wellness modules
│   ├── data/                 # Sample data and templates
│   │   └── text_files/       # Text files for prompts and documentation
│   ├── generated_output/     # Generated wellness plans and PDFs
│   ├── static/               # Static assets
│   │   ├── css/              # CSS files
│   │   ├── js/               # JavaScript files
│   │   └── img/              # Images and icons
│   ├── templates/            # HTML templates
│   └── utils/                # Utility functions (email, WhatsApp)
├── config/                   # Configuration files
├── logs/                     # Log files
└── tests/                    # General test files
```

## Features

- Generate personalized wellness plans with Cohere AI integration
- Dashboard for managing client wellness plans
- PDF export functionality
- WhatsApp and email communication capabilities
- Gujarati/Indian dietary recommendations

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/HRIMWellness.git
   cd HRIMWellness
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in `config/.env`

## Usage

Run the application:

```
python -m app.app
```

Access the dashboard at http://localhost:5000

## Development

1. The main application flow starts in `app/app.py`
2. Core wellness plan generation is in `app/core/wellness/generate_wellness_pdf.py`
3. Dashboard UI is in `app/templates/dashboard.html`

## Testing

Run tests:

```
python -m pytest tests/
```

## Wellness Plan Generator

The application includes a wellness plan generator that creates personalized wellness and diet plans based on user information.

### Usage

You can generate wellness plans in several ways:

1. **Web Interface**
   
   Run the web interface:
   ```
   python generate_wellness.py --web
   ```
   
   Then access the wellness form at: http://localhost:5000/wellness_form

2. **Command Line with Random Data**
   
   Generate a plan with random data:
   ```
   python generate_wellness.py --random
   ```

3. **Command Line with Input File**
   
   Generate a plan with specific data from a JSON file:
   ```
   python generate_wellness.py --input tests/sample_user_data.json
   ```

4. **Generate PDF Output**
   
   Add the `--pdf` flag to generate a PDF (requires WeasyPrint):
   ```
   python generate_wellness.py --random --pdf
   ```

All generated plans are saved in the `generated_data` directory by default, but you can specify a different output directory with the `--output` parameter.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
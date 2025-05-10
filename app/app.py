import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define paths for generated data
def get_generated_data_path():
    """
    Returns the path to store generated output
    Checks both app structure and root locations
    """
    # Option 1: App structure path
    app_path = os.path.join(os.path.dirname(__file__), 'generated_output')
    
    # Option 2: Root path
    root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated_data')
    
    # Check which one exists and return it
    if os.path.exists(root_path):
        return root_path
    else:
        return app_path

# Set the environment variable for generated data path
os.environ['GENERATED_DATA_PATH'] = get_generated_data_path()

# Import the Flask app
from app.core.dashboard_server import app

if __name__ == "__main__":
    print(f"Using generated data path: {os.environ.get('GENERATED_DATA_PATH')}")
    app.run(debug=True) 
import os

# Path options for the llm_prompt.txt file
def get_llm_prompt_path():
    """
    Returns the path to the llm_prompt.txt file
    Tries both the app/data/text_files location and the root text_files location
    """
    # Option 1: App structure path
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'text_files', 'llm_prompt.txt')
    
    # Option 2: Root path
    root_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'text_files', 'llm_prompt.txt')
    
    # Check which one exists and return it
    if os.path.exists(root_path):
        return root_path
    else:
        return app_path
        
# For backward compatibility
LLM_PROMPT_PATH = get_llm_prompt_path() 
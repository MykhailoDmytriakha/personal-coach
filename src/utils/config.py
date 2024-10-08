import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    user_data_dir = os.path.join(base_dir, 'user_data')

    config = {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'openai_gpt_model': os.getenv('OPENAI_GPT_MODEL', 'gpt-4o'),
        'openai_gpt_model_small': os.getenv('OPENAI_GPT_MODEL_SMALL', 'gpt-4o-mini'),
        'openai_whisper_model': os.getenv('OPENAI_WHISPER_MODEL', 'whisper-1'),
        'user_data_folder': user_data_dir,
        'recordings_folder': os.path.join(user_data_dir, 'recordings'),
        'debug_mode': os.getenv('DEBUG_MODE', 'False').lower() == 'true',
        'default_language': os.getenv('DEFAULT_LANGUAGE', 'en'),
        'DB_NAME': 'user_data.db'
    }

    # Ensure required folders exist
    os.makedirs(config['user_data_folder'], exist_ok=True)
    os.makedirs(config['recordings_folder'], exist_ok=True)

    # Validate critical configuration
    if not config['openai_api_key']:
        raise ValueError("OpenAI API key is not set. Please set OPENAI_API_KEY in your environment or .env file.")

    return config

def get_config():
    """
    Singleton-like function to get or create configuration.
    """
    if not hasattr(get_config, 'config'):
        get_config.config = load_config()
    return get_config.config

# Additional utility functions can be added here
def update_config(key, value):
    """
    Update a specific configuration value.
    """
    config = get_config()
    config[key] = value

def get_config_value(key, default=None):
    """
    Get a specific configuration value.
    """
    config = get_config()
    return config.get(key, default)
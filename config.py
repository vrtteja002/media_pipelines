import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AUDIO_OUTPUT_DIR = "outputs/audio"
    JSON_OUTPUT_DIR = "outputs/json"
    TEMP_DIR = "temp"
    
    # Ensure directories exist
    for dir_path in [AUDIO_OUTPUT_DIR, JSON_OUTPUT_DIR, TEMP_DIR]:
        os.makedirs(dir_path, exist_ok=True)
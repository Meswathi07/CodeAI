from dotenv import load_dotenv
import os

load_dotenv()

def get_api_key():
    return os.getenv("GEMINI_API_KEY")

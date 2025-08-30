import os
from dotenv import load_dotenv
import openai

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment.")
    
    return openai.OpenAI(api_key=api_key, base_url=base_url)

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY", "")
    base_url = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment.")
    
    return openai.OpenAI(api_key=api_key, base_url=base_url)

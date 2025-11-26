from openai import OpenAI
from Config.settings import OPENROUTER_KEY , GEMINI_KEY

def get_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= OPENROUTER_KEY
    )

def get_gemini():
    return OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=GEMINI_KEY,
)
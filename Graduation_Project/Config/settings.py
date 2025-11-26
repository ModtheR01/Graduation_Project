import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv("Deep_Seek_key_OpenRouter")
GEMINI_KEY = os.getenv("Gemini_key")
Amadeus_BaseURL= os.getenv("AMADEUS_BASE_URL")
Amadeus_Key = os.getenv("Amadeus_APIKEY")
Amadeus_SecretKey = os.getenv("Amadeus_APISecret")
Deep_Seek_key=os.getenv("Deep_Seek_key")

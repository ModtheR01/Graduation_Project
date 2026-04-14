import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv("OpenRouter_key")
GEMINI_KEY = os.getenv("Gemini_key")
Amadeus_BaseURL= os.getenv("AMADEUS_BASE_URL")
Amadeus_Key = os.getenv("Amadeus_APIKEY")
Amadeus_SecretKey = os.getenv("Amadeus_APISecret")
Deep_Seek_key=os.getenv("Deep_Seek_key")
Stripe_Publishable=os.getenv("STRIPE_PUBLISHABLE")
Stripe_Secret=os.getenv("STRIPE_SECRET")
Stripe_Webhook_Secret=os.getenv("STRIPE_WEBHOOK_SECRET")
XRapidAPIKey=os.getenv("XRapidAPIKey")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
AUTH_GOOGLE_CLIENT_ID = os.getenv("AUTH_GOOGLE_CLIENT_ID")
AUTH_GOOGLE_CLIENT_SECRET = os.getenv("AUTH_GOOGLE_CLIENT_SECRET")
AUTH_GOOGLE_REDIRECT_URI = os.getenv("AUTH_GOOGLE_REDIRECT_URI")
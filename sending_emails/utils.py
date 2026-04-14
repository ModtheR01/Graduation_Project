import time
import urllib.parse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import requests
from django.utils import timezone as tz
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from Graduation_Project.Users.models import User
from .models import Contacts , Tokens
import os
from dotenv import load_dotenv
import jwt
load_dotenv()


# contacts related functions

def get_all_contacts(request):
    try:
        contacts = Contacts.objects.filter(user_email=request.user)
        absstracted_contacts = [] # we want to return only the email and the name not the whole object with all its attributes to not confuse the stupid model 
        for contact in contacts:
            absstracted_contacts.append({   
                "receiver_email": contact.receiver_email,
                "nickname": contact.nickname,
            })
    except Contacts.DoesNotExist:
        return "this user has no contacts yet, please ask him to add some contacts first " 

def add_contact(request,email,name):
    try:
        new_contact = Contacts.objects.create(user_email=request.user,receiver_email=email,nickname=name)
        new_contact.save()
        return {"receiver_email": new_contact.receiver_email,"nickname": new_contact.nickname}
    except Exception as e:
        print(f"Error occurred while adding new contact: {e}")
        return "Error occurred while adding new contact"
    
def is_email_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# email task related funtions :

GOOGLE_CLIENT_ID= os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET= os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI= os.getenv("GOOGLE_REDIRECT_URI")
OAUTH_AUTH_URL= os.getenv("OAUTH_AUTH_URL")
OAUTH_TOKEN_URL= os.getenv("OAUTH_TOKEN_URL")
# this scope tells gmail that we will only use user token to send emails
SCOPE = "https://www.googleapis.com/auth/gmail.send"



def build_auth_url(user):
    sk =os.getenv("FERNET_KEY")
    if not sk:
        raise ValueError("FERNET_KEY environment variable is not set")
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",       # makes google return a code within the url
        "scope": SCOPE,
        "access_type": "offline",      # so we get a refresh_token instead of asking user to login again
        "prompt": "consent",           # force showing consent screen even if the user gave consent before
        "state": jwt.encode({"user_id": user.id}, sk, algorithm="HS256")  # encode user id in the state param to identify the user when google redirects back to our app
    }
    # this link should be returned to hassan so he call it on the frontend to show conscent screen
    return f"{OAUTH_AUTH_URL}?{urllib.parse.urlencode(params)}"

def exchange_code_for_tokens(code: str):
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code", #tells Google we’re doing the standard code exchange.
        # we can set it to refresh_token --> use an existing refresh token to get a new access token 
        # and many more grant types that tells google what are we exchanging the code for
    }
    if OAUTH_TOKEN_URL is None or GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None or GOOGLE_REDIRECT_URI is None:
        raise ValueError("One or more required environment variables are not set")
    if code is None:
        raise ValueError("Authorization code is not sent in the request to exchange for tokens")
    
    resp = requests.post(OAUTH_TOKEN_URL, data=data) #sends a POST request to the token endpoint with the data payload.
    #throws an exception if HTTP status is not 2xx.
    resp.raise_for_status()
    token_data = resp.json() #converts the JSON response body to a Python dict.

    # Compute an absolute expiry time (UNIX timestamp)
    expires_in = token_data.get("expires_in", 0)
    token_data["expires_at"] = int(time.time()) + int(expires_in) - 60  # minus 60 seconds as buffer

    return token_data

def save_tokens(user_id, token_data: dict):
    user = User.objects.get(id=user_id)

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_at = token_data.get("expires_at")

    if not refresh_token or not expires_at:
        raise ValueError("No refresh token or expiry time returned from Google")

    expiry_datetime = datetime.fromtimestamp(expires_at, tz=timezone.utc)

    token_obj, created = Tokens.objects.get_or_create(user=user)

    token_obj.access_token = access_token

    # ⚠️ Google ساعات مش بترجع refresh_token تاني
    if refresh_token:
        token_obj.refresh_token = refresh_token

    token_obj.expiry = expiry_datetime
    token_obj.save()

def get_valid_access_token(user):

    token_obj = Tokens.objects.get(user=user)

    # لو لسه valid
    if token_obj.expiry > tz.now():
        return token_obj.get_access_token()

    # ❌ expired → نعمل refresh
    refresh_token = token_obj.get_refresh_token()

    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    if not OAUTH_TOKEN_URL or not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("One or more required environment variables are not set")
    resp = requests.post(OAUTH_TOKEN_URL, data=data)
    resp.raise_for_status()
    token_data = resp.json()

    new_access_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in", 0)

    # update DB
    token_obj.access_token = new_access_token
    token_obj.expiry = tz.now() + tz.timedelta(seconds=expires_in - 60)
    token_obj.save()

    return new_access_token

def get_gmail_service(request):
    access_token = get_valid_access_token(user=request.user)

    if not access_token:
        raise RuntimeError("Failed to obtain valid access token.")

    token_obj = Tokens.objects.get(user=request.user)
    refresh_token = token_obj.get_refresh_token()

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )

    service = build("gmail", "v1", credentials=creds)
    return service
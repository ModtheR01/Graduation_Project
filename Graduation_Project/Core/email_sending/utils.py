import json
import time
import requests
from typing import Dict

from Core.email_sending.config import GOOGLE_CLIENT_ID , GOOGLE_CLIENT_SECRET

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from Core.email_sending.config import  GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, TOKENS_FILE



# google api that deals with tokens
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"

# almost all of them are temporary sol until we add db then the token will be linked with the user id

# doing it manualy

{
"""

# load all tokens from tokens.json
def load_tokens() -> Dict:
    #Load token data from tokens.json into a Python dict.
    with open(TOKENS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
# save the token back in the file
def save_tokens(token_data: Dict) -> None:
    #Save token data back to tokens.json.
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)

def get_remaining_lifetime(token_data: Dict) -> int:
   
    #Return how many seconds are left before the access_token expires.
    #If negative or zero => already expired.
    
    now = int(time.time())
    expires_at = int(token_data.get("expires_at", 0))
    remaining = expires_at - now
    return remaining

def is_expired(token_data: Dict, buffer_seconds: int = 60) -> bool:
    
    #Return True if token is already expired or will expire within buffer_seconds.
    #This helps us refresh a bit before actual expiry.
    
    remaining = get_remaining_lifetime(token_data)
    return remaining <= buffer_seconds

def refresh_access_token(token_data: Dict) -> Dict:
    
    #Use the refresh_token to obtain a new access_token from Google.
    #Update token_data with new access_token and expires_at, then save to file.
    
    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("No refresh_token found.")

    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(OAUTH_TOKEN_URL, data=data)
    response.raise_for_status()
    new_data = response.json()

    # Google returns a new access_token and expires_in
    new_access_token = new_data["access_token"]
    expires_in = int(new_data.get("expires_in", 0))

    # Update old token_data, keep existing refresh_token
    token_data["access_token"] = new_access_token
    token_data["expires_at"] = int(time.time()) + expires_in - 60  # small buffer

    # Persist to disk
    save_tokens(token_data)

    return token_data

"""
}
    

#Returns an authenticated Gmail API service using saved tokens.json.
# this service is like python wrapper it automate creating http request from headers and payload and parsing
def get_gmail_service():
    with open(TOKENS_FILE, "r") as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )

    # Google automatically refreshes access_token if expired
    # this create a python object that can call google gmail service v1 using specific user creds.
    service = build("gmail", "v1", credentials=creds)
    return service
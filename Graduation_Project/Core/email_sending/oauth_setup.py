""" 
this file wont be used in production we are only using it as one time verification with google 
to get my access token and refresh token (temporary solution)
when hassan build the ui the process will happen as:
- the user get redirected to google consent page 
- the user give permission to us to use his email to send mails
- google send a code to the specified uri of "http://localhost:8000/oauth2callback"
- with that code and the client secret we will contact google to get the user`s access token 
- we use his token to send mails directly from his gmail on his behalf

"""

import http.server
import socketserver
import urllib.parse
import webbrowser
import json
import time
import requests

from Core.email_sending.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, TOKENS_FILE

OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"

# this scope tells gmail that we will only use user token to send emails
SCOPE = "https://www.googleapis.com/auth/gmail.send"


def build_auth_url():
    """
    Build the Google OAuth URL that will:
    - show the consent screen to the user
    - ask for permission to send emails (gmail.send scope)
    """
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",       # makes google return a code within the url
        "scope": SCOPE,
        "access_type": "offline",      # so we get a refresh_token instead of asking user to login again
        "prompt": "consent",           # force showing consent screen even if the user gave consent before
    }
    # urllib.parse.urlencode turn this dict into a url query string 
    return f"{OAUTH_AUTH_URL}?{urllib.parse.urlencode(params)}"


class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    """
    This tiny HTTP handler will receive Google's redirect request:
      GET /oauth2callback?code=...

    We grab ?code=..., save it in a class variable, and show a simple message.
    """

    code_received = None  # class variable to store the code

    # function to handle only GET request 
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # We only care about the exact redirect path we configured
        if parsed.path != "/oauth2callback":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        # Extract the "code" query parameter
        qs = urllib.parse.parse_qs(parsed.query)
        if "code" not in qs:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'code' in query parameters")
            return

        code = qs["code"][0]
        OAuthHandler.code_received = code

        # Respond to the browser so you see something nice
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization success! You can close this tab and go back to your terminal.")

    # Disable noisy logging in console because SimpleHTTPRequestHandler by default logs every request (IP, path, etc.) to the console
    def log_message(self, format, *args):
        return


def run_local_server():
    """
    Start a very small HTTP server on localhost:8000
    to catch Google's redirect with the authorization code.
    """
    parsed = urllib.parse.urlparse(GOOGLE_REDIRECT_URI)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8000

    with socketserver.TCPServer((host, port), OAuthHandler) as httpd:
        print(f"[OAuth] Listening on {host}:{port} for callback...")
        # handle_request() will block until a single request is served
        httpd.handle_request()


def exchange_code_for_tokens(code: str):
    """
    Take the authorization code and exchange it for:
    - access_token
    - refresh_token
    - expires_in
    Using Google's token endpoint.
    """
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code", #tells Google we’re doing the standard code exchange.
        # we can set it to refresh_token --> se an existing refresh token to get a new access token 
        # and many more grant types that tells google what are we exchanging the code for
    }

    resp = requests.post(OAUTH_TOKEN_URL, data=data)
    #throws an exception if HTTP status is not 2xx.
    resp.raise_for_status()
    token_data = resp.json() #converts the JSON response body to a Python dict.

    # Compute an absolute expiry time (UNIX timestamp)
    expires_in = token_data.get("expires_in", 0)
    token_data["expires_at"] = int(time.time()) + int(expires_in) - 60  # minus 60 seconds as buffer

    return token_data


def save_tokens(token_data: dict):
    """
    Save tokens to tokens.json so we can reuse them later.
    """
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)
    print(f"[OAuth] Tokens saved to {TOKENS_FILE}")
    print(f"tokens:{token_data}")


def main():
    # 1) Build the Google OAuth URL
    auth_url = build_auth_url()
    print("[OAuth] Open this URL in your browser (if it doesn't open automatically):")
    print(auth_url)
    print()

    # 2) Try to open the browser automatically
    webbrowser.open(auth_url)

    # 3) Start local server and wait for Google to redirect with ?code=...
    run_local_server()

    # 4) After redirect, the handler should have stored the code
    if not OAuthHandler.code_received:
        print("[OAuth] No code received. Did you approve the consent screen?")
        return

    code = OAuthHandler.code_received
    print(f"[OAuth] Got authorization code: {code[:10]}...")

    # 5) Exchange code for tokens
    token_data = exchange_code_for_tokens(code)
    print("[OAuth] Received tokens from Google:")
    print(json.dumps(token_data, indent=2))

    # 6) Save tokens to file
    save_tokens(token_data)

    print("[OAuth] Setup complete. You won't need to do this often.")


if __name__ == "__main__":
    main()

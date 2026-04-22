import requests
import os
from chat.api_keys import SENDGRID_API_KEY

def send_reset_email(to_email, reset_link):
    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": "romee.agent@gmail.com", "name": "Romee"},
            "subject": "Reset Your Password",
            "content": [{"type": "text/plain", "value": f"Click here to reset your password:\n{reset_link}"}]
        }
    )
    print("SendGrid status:", response.status_code)
    print("SendGrid response:", response.text)
    return response
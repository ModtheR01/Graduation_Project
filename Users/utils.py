import requests
import os

def send_reset_email(to_email, reset_link):
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": os.getenv("BREVO_API_KEY"),
            "Content-Type": "application/json"
        },
        json={
            "sender": {"name": "Romee", "email": "romee.agent@gmail.com"},
            "to": [{"email": to_email}],
            "subject": "Reset Your Password",
            "textContent": f"Click here to reset your password:\n{reset_link}"
        }
    )
    print("Brevo status:", response.status_code)
    print("Brevo response:", response.json())
    return response
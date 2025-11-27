from Core.email_sending.utils import get_gmail_service
from email.mime.text import MIMEText
import base64
from langchain_core.tools import tool

@tool
def send_email(to, subject, body,is_approved:False):
    """
    Send an email using Gmail.

    Use this tool whenever the user asks to send an email, write an email, or deliver a message via email.

    Required parameters:
    - to: recipient's email address (must be a valid email format, e.g., "example@gmail.com")
    - subject: short subject line summarizing the email's purpose
    - body: full message content to be included in the email body
    - is_approved: check if the user approved the drafted email before actually sending it

    The tool does not return anything, but assumes the email is successfully sent.
    """

    service = get_gmail_service()
    
    # Create MIME email
    # telling the api the body is in plain text not html also createing the mime object to hold other data
    mime = MIMEText(body, "plain", "utf-8")
    mime["to"] = to
    mime["subject"] = subject

    # turn the mail to bytes (mime.as_bytes()) then encode it to base64 then turn it to string(decode("utf-8"))
    raw_message = base64.urlsafe_b64encode(mime.as_bytes()).decode("utf-8")

    #the api expect it in json format of {"raw:xqcadpj4d6ada5sc46a865c "}
    message = {"raw": raw_message}

    if is_approved:
        # Send email
        sent_message = service.users().messages().send(
            userId="me", body=message
        ).execute()
        print("📧 Email sent! ID:", sent_message["id"])
    else:
        print("need to ask user for approval")


from flights.state_store import get_store

from .utils import get_gmail_service
from email.mime.text import MIMEText
import base64
from langchain_core.tools import tool
from sending_emails.utils import get_all_contacts ,add_contact
from .utils import is_email_valid 

@tool
def search_in_contact(request):
    """
    use this tools whenever user want to send email to someone but provided a name not an email address
    this fucntion return a list of all available contact in the database so you can compare the name you got with the list of names here 
    to get the associated email

    this tool will provide you with the list of contacts of the user

    parameters: 
    request: the request object to get the user email and search for his contacts in the db
    (send it as is from the frontend without extracting any data from it the function will handle that)

    for example : "send email to ahmed"

    return example: [{"name":"ahmed","email":"ahmed@example.com"},{"name":"modather","email":"modatherosama@example.com"}]

    if the name is not found in the db tell the user to provide the email again and its associated name and save it by calling the function add_new_contact from your tools
    """
    try :
        list_contact = get_all_contacts(request)
        return list_contact
    except:
        print("Error occurred while fetching contacts")
        return "tell the user there is currently a proplem with fetching his contacts, please try again later or add the contact you want to send email to manually from the dashboard"

@tool
def add_new_contact(request, name, email):
    """
    use this tools whenever user want to save new contact by providing "email_address" and "name"

    parameters:
    email: the new email address the user want to save 
    name : the name associated with the email contact in db

    this fucntion return the new contact
    for example : "save this contact anas.say3d@gmail.com under name anas"

    """
    is_email_valid(email)
    new_contact = add_contact(request,name,email)
    print(new_contact)
    return new_contact



@tool
def send_email( to, subject, body, is_approved=False):
    """
    Never Send any email before making a draft and showing it to the user and the user must agree to send it 
    
    Send an email using Gmail.

    Use this tool whenever the user asks to send an email, write an email, or deliver a message via email.

    
    Required parameters:
    - to: recipient's email address (must be a valid email format, e.g., "example@gmail.com")
    - subject: short subject line summarizing the email's purpose
    - body: full message content to be included in the email body
    - is_approved: check if the user approved the drafted email before actually sending it

    The tool does not return anything, but assumes the email is successfully sent.
    """

    print("initializing Gmail service... step 3")
    store = get_store()
    user_id = store.get("user_id")
    print("user_id in send_email:", user_id, "type:", type(user_id), "to:", to, "subject:", subject, "body:", body, "is_approved:", is_approved)
    service = get_gmail_service(user_id)
    print("Gmail service initialized successfully.")
    
    # Create MIME email
    # telling the api the body is in plain text not html also createing the mime object to hold other data
    mime = MIMEText(body, "plain", "utf-8")
    mime["to"] = to
    mime["subject"] = subject
    print("formating email...")
    # turn the mail to bytes (mime.as_bytes()) then encode it to base64 then turn it to string(decode("utf-8"))
    raw_message = base64.urlsafe_b64encode(mime.as_bytes()).decode("utf-8")

    #the api expect it in json format of {"raw:xqcadpj4d6ada5sc46a865c "}
    message = {"raw": raw_message}
    print("checking approval...")
    if is_approved:
        try:
            # Send email (this is normal post api request managed by google sdk)
            sent_message = service.users().messages().send(
                userId="me", body=message
            ).execute()
            print("📧 Email sent! ID:", sent_message["id"])
            return ({"📧 Email sent! ID:":sent_message["id"]})
        except:
            print("Google api isnt responding right now, please try later! ")
            return ({"error":"Google api isnt responding right now, please try later!"})
        
    else:
        print("need to ask user for approval")
        return ({"error":"need to ask user for approval."})



# alter the database to add the task of sending email when the email is sent alter this function to be production ready
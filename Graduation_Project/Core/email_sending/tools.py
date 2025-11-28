from Core.email_sending.utils import get_gmail_service
from email.mime.text import MIMEText
import base64
from langchain_core.tools import tool
from Core.email_sending.mock_contact import contact_list

# basic tools that will change with addotion of db

@tool
def search_in_contact():
    """
    use this tools whenever user want to send email to someone but provided a name not an email address
    this fucntion return a list of all available contact in the database so you can aompare the name you got with the list of names here 
    to get the associated email

    for example : "send email to ahmed"

    return example: [{"name":"ahmed","email":"ahmed@example.com"},{"name":"modather","email":"modatherosama@gmail.com"}]

    if the name is not found in the db tell the user to provide the email again and its associated name and save it by calling the function add_new_contact from your tools
    """
    # TODO actual contact retrieval from db
    list_contact=[]
    for contact in contact_list:
        list_contact.append({"name":contact["name"],"email":contact["email"]})
    print("done searching returning list of contact...")
    return list_contact


@tool
def add_new_contact(name,email):
    """
    use this tools whenever user want to save new contact by providing "email_address" and "name"

    parameters:
    email: the new email address the user want to save 
    name : the name associated with the email contact in db

    this fucntion doesnt return anything so act as if it is already added 

    for example : "save this contact anas.say3d@gmail.com under name anas"

    """
    # TODO: validate email , name
    # TODO: store the actual data in the DB
    contact_list.append({"id":contact_list[-1]["id"]+1,"name":name,"email":email})
    print(contact_list)



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
    print("formating email...")
    # turn the mail to bytes (mime.as_bytes()) then encode it to base64 then turn it to string(decode("utf-8"))
    raw_message = base64.urlsafe_b64encode(mime.as_bytes()).decode("utf-8")

    #the api expect it in json format of {"raw:xqcadpj4d6ada5sc46a865c "}
    message = {"raw": raw_message}
    print("checking approval...")
    if is_approved:
        # Send email
        sent_message = service.users().messages().send(
            userId="me", body=message
        ).execute()
        print("📧 Email sent! ID:", sent_message["id"])
    else:
        print("need to ask user for approval")

    print("end of tool(send_email)...")


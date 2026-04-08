from .models import Contacts

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
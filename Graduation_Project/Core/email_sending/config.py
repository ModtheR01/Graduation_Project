import os
from dotenv import load_dotenv
load_dotenv()


GOOGLE_CLIENT_ID= os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET= os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI= os.getenv("GOOGLE_REDIRECT_URI")
OWNER_EMAIL= os.getenv("OWNER_EMAIL")
TOKENS_FILE= os.getenv("TOKENS_FILE")

# data of my gmail just for testing sending mails this will be stored in db for every single user 
# (tell jo to alter tha database desogn to include user tokens)
# مدثر اعمل ران لفايل oauth_setup وهات الداتا من tokens.json 

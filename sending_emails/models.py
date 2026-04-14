from django.db import models
from Tasks.models import Tasks
from Users.models import User
from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
import os

# Create your models here.
class Contacts(models.Model):
    receiver_email = models.CharField(max_length=50)
    user_email = models.ForeignKey(User, models.CASCADE, db_column='user_email')
    nickname = models.CharField(max_length=30)
    contact_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'contacts'
        unique_together = (('nickname', 'contact_id'),)


class Email(models.Model):
    pk = models.CompositePrimaryKey('task_id', 'to_email')
    task = models.OneToOneField(Tasks, models.DO_NOTHING)
    to_email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'email'




# the user tokens for sending emails :
# 🔐 encryption setup
FERNET_KEY = os.getenv("FERNET_KEY")  
if not FERNET_KEY:
    raise ValueError("FERNET_KEY is not set in the environment variables.")
cipher = Fernet(FERNET_KEY.encode())


class Tokens(models.Model):
    user_email = models.ForeignKey(User, models.CASCADE, db_column='user_email')

    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True,null=True)

    expiry = models.DateTimeField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔐 encrypt before save
    def save(self, *args, **kwargs):
        if self.refresh_token and not self.refresh_token.startswith("gAAAA"):
            self.refresh_token = cipher.encrypt(self.refresh_token.encode()).decode()
    
        if self.access_token and not self.access_token.startswith("gAAAA"):
            self.access_token = cipher.encrypt(self.access_token.encode()).decode()

        super().save(*args, **kwargs)

    # 🔓 decrypt helpers
    def get_refresh_token(self):
        return cipher.decrypt(self.refresh_token.encode()).decode()

    def get_access_token(self):
        if not self.access_token:
            return None
        return cipher.decrypt(self.access_token.encode()).decode()
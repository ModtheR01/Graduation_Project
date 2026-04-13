import threading

from django.db import models
from Users.models import User



class Chats(models.Model):
    user_email = models.ForeignKey(User, models.DO_NOTHING, db_column='user_email')
    title = models.CharField(max_length=50, blank=True, null=True)
    message = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        managed = True
        db_table = 'chats'

message_example = [{"role":"user","content":"Hello!"}]
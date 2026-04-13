import threading

from django.db import models
from Users.models import User
from .utils import generate_title


class Chats(models.Model):
    user_email = models.ForeignKey(User, models.DO_NOTHING, db_column='user_email')
    title = models.CharField(max_length=50, blank=True, null=True)
    message = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        managed = True
        db_table = 'chats'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
    
        super().save(*args, **kwargs)
    
        if is_new and not self.title:
            def generate():
                title = generate_title(self.message["user"])
                self.title = title
                self.save(update_fields=["title"])
    
            threading.Thread(target=generate).start()

message_example = {"user":"message"}
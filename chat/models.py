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

        if is_new and not self.title and self.message:
            def generate(chat_id, message):
                user_message = message[0]["content"]

                title = generate_title(user_message)

                # update بدون ما ننادي save تاني
                Chats.objects.filter(pk=chat_id).update(title=title)

            threading.Thread(target=generate, args=(self.pk, self.message)).start()

message_example = [{"role":"user","content":"Hello!"}]
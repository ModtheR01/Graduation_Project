from django.db import models
from chat.models import Chats
# Create your models here.
class Tasks(models.Model):
    chat = models.ForeignKey(Chats, models.CASCADE, db_column='chat_id')
    task_type = models.CharField(max_length=15, blank=True, null=True)
    offer_data = models.JSONField(null=True, blank=True)  
    booking_data = models.JSONField(null=True, blank=True)  
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tasks'
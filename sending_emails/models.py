from django.db import models
from Tasks.models import Tasks
from Users.models import User

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
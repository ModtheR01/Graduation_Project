from django.db import models
from Tasks.models import Tasks

# Create your models here.
class Reminder(models.Model):
    pk = models.CompositePrimaryKey('task_id', 'title')
    task = models.OneToOneField(Tasks, models.CASCADE, db_column='task_id')
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True, null=True)
    reminder_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'reminder'
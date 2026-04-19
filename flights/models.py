from django.db import models
from Tasks.models import Tasks


# Create your models here.
class Traveling(models.Model):
    ticket_num = models.CharField(max_length=20, primary_key=True)
    task = models.OneToOneField(Tasks, models.CASCADE, db_column='task_id')
    origin = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    departure_date = models.CharField(blank=True, null=True)
    departure_time = models.CharField(blank=True, null=True)
    return_time = models.CharField(blank=True, null=True)
    number_of_passengers = models.IntegerField(blank=True, null=True)
    moving_method = models.CharField(max_length=15, blank=True, null=True)
    moving_service_provider = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'traveling'
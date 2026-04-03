from django.db import models
from Tasks.models import Tasks

# Create your models here.
class Hotels(models.Model):
    booking_number = models.CharField(primary_key=True, max_length=30)
    task = models.OneToOneField(Tasks, models.DO_NOTHING)
    number_of_persons = models.IntegerField(blank=True, null=True)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    hotel_name = models.CharField(max_length=40, blank=True, null=True)
    check_in_date = models.DateTimeField(blank=True, null=True)
    check_out_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hotels'
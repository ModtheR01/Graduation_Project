from django.db import models
from Tasks.models import Tasks

# Create your models here.
class ToDoList(models.Model):
    list_name = models.CharField(primary_key=True, max_length=50)
    task = models.OneToOneField(Tasks, models.CASCADE , null=True, blank=True)
    finished = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'to_do_list'


class ToDoItems(models.Model):
    pk = models.CompositePrimaryKey('list_name', 'item_name')
    list_name = models.ForeignKey('ToDoList', models.CASCADE, db_column='list_name')
    item_name = models.CharField(max_length=30)
    finished = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'to_do_items'
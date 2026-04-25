from django.db import models
from Tasks.models import Tasks
from Users.models import User

# Create your models here.
class ToDoList(models.Model):
    list_name = models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, models.CASCADE)
    task = models.OneToOneField(Tasks, models.DO_NOTHING , null=True, blank=True)
    finished = models.BooleanField(blank=True, null=True ,default=False)

    class Meta:
        managed = True
        db_table = 'to_do_list'
        unique_together = ('user', 'list_name')


class ToDoItems(models.Model):
    list_name = models.ForeignKey('ToDoList', models.CASCADE, db_column='list_name')
    item_name = models.CharField(max_length=30)
    finished = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        managed = True
        db_table = 'to_do_items'
        unique_together = ('list_name', 'item_name')
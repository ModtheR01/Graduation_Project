from django.contrib import admin
from .models import ToDoItems,ToDoList

# Register your models here.
admin.site.register(ToDoList)
# admin.site.register(ToDoItems) #cannot registered because it has a composite pk and django does not support it in admin panel 
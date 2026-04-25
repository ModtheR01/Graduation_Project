from .models import ToDoList,ToDoItems
from rest_framework import serializers

class todoList_serializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__'

class todoList_items_serializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItems
        fields = '__all__'
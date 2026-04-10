from .models import Contacts
from rest_framework import serializers

class contact_serializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'
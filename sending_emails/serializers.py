from .models import Contact
from rest_framework import serializers

class contact_serializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
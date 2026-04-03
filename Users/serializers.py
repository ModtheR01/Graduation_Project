# Users/serializers.py
from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer): # ModelSerializer => use it when we will want to interact with DB (ex -> CRUD operations)
    class Meta:
        model = User
        fields = ['email', 'password', 'fname', 'lname', 'phone_number', 
                'country', 'city', 'street', 'birth_date', 'country_code']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer): # Serializer => it is just as a form to receive the values from the user and validate it
    email = serializers.EmailField() # check the email valid or not (Email Validation) 
    password = serializers.CharField() # check if the value is string or not (String Validation)
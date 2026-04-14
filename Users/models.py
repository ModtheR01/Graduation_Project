from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin

class UserManager(BaseUserManager): # our manager 
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        # if not phone_number:
        #     raise ValueError("Users must have a phone number") # because we set it as required field in our model
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password) # hash the password
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):  #this function must has this name because when we will create a superuser we will use it in terminal 'python manage.py createsuperuser'
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin): # this class must inherit from AbstractBaseUser and PermissionsMixin to tell django that 'this table has login and permissions ,....' and [AbstractBaseUser provides the core authentication logic (password hashing, login handling),but leaves user fields and structure fully customizable (e.g., use email instead of username).]
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    phone_number = models.CharField(unique=True, max_length=11,blank=True, null=True)
    country = models.CharField(max_length=15,blank=True, null=True)
    city = models.CharField(max_length=20,blank=True, null=True)
    street = models.CharField(max_length=30,blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=5,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() # makes 'objects' use our manager
    USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = ["phone_number"] # this field will be required when we create superuser from terminal

    class Meta:
        managed = True
        db_table = 'users'
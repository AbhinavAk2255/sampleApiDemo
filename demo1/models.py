from datetime import timedelta
import re
from django.contrib.auth.models import Permission,Group
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.forms import ValidationError
from django.utils import timezone
import random
from django.core.validators import RegexValidator
import phonenumbers
from django.conf import settings
import uuid
from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError
import uuid


# Create your models here.
phone_regex = RegexValidator(
        regex=r'^\d{9,15}$', 
        message="Phone number must be between 9 and 15 digits."
    )

def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760:  # 10 MB
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    return value

class Country_Codes(models.Model):
    country_name = models.CharField(max_length=100,unique=True)
    calling_code = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f"{self.country_name} ({self.calling_code})"
    
    class Meta:
        ordering = ['calling_code']



class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class District(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be provided')

        # Normalize the email if provided
        if email:
            email = self.normalize_email(email)

        # Handle phone number validation if provided and not a superuser
        # if phone_number and not extra_fields.get('is_superuser'):
        #     full_number = f"{extra_fields.get('country_code')}{phone_number}"
        #     try:
        #         parsed_number = phonenumbers.parse(full_number, None)
        #         if not phonenumbers.is_valid_number(parsed_number):
        #             raise ValidationError("Invalid phone number.")
        #         phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        #     except phonenumbers.NumberParseException:
        #         raise ValidationError("Invalid phone number format.")

        # Create and return the user object
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if email is None:
            raise ValueError('Superuser must have an email address.')

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)
    


class User(AbstractBaseUser):
    created_at = models.DateTimeField(auto_now_add=True)
    # Role-based fields
    is_franchisee = models.BooleanField(default=False)


    # Any other fields common to both roles
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=30)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=10)
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)
    watsapp = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    country_code = models.ForeignKey('Country_Codes', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    objects = UserManager()



    def __str__(self):
        return self.email if self.email else self.phone_number


class Franchise_Type(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50,default="INR")


class Franchisee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='franchasees')

    about = models.TextField()
    profile_image = models.ImageField(upload_to='f-profile_images/', null=True, blank=True)  # Profile image field
    revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dealers = models.IntegerField(blank=True, null=True)
    service_providers = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey(Franchise_Type, on_delete=models.CASCADE,related_name='franchisee_type')

    valid_from = models.DateTimeField(null=True, blank=True)
    valid_up_to = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    verification_id = models.CharField(max_length=255, blank=True, null=True)  
    verificationid_number = models.CharField(max_length=50, blank=True, null=True)  # ID number field
    community_name = models.CharField(max_length=50)



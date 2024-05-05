from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
# Extend Customer user(Default by django) w/ Abstract user
# This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises
# add your own profile fields and methods. AbstractBaseUser only contains the authentication functionality, but no actual fields

from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



class Customer(AbstractUser):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1,blank=True, choices=GENDER_CHOICES)
    birthdate = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    username = None
    # login with email because if we don't do that django make login by username by default
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []

    objects = MyUserManager() 

    def __str__(self):

        return self.name


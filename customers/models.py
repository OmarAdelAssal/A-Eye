# from django.db import models
# from django.utils import timezone

# from django.contrib.auth.models import AbstractUser
# # Extend Customer user(Default by django) w/ Abstract user
# # This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises
# # add your own profile fields and methods. AbstractBaseUser only contains the authentication functionality, but no actual fields
# class Customer(AbstractUser):

#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )

#     name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20, blank=True)
#     gender = models.CharField(max_length=1,blank=True, choices=GENDER_CHOICES)
#     birthdate = models.DateField(blank=True, null=True)
#     address = models.TextField(blank=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     username = None
#     # login with email because if we don't do that django make login by username by default
#     USERNAME_FIELD = 'email' 
#     REQUIRED_FIELDS = [] 


#     def __str__(self):

#         return self.name
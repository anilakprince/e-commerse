from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    GENDER_CHOICES=[
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]

    name = models.CharField(max_length=50,default='Anonymous')
    email = models.EmailField(max_length=250,unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M')
    date_of_birth = models.DateField(null=True,blank=True)
    password = models.CharField(max_length=8, null=True)
    session_token = models.CharField(max_length=10,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    username= None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.name
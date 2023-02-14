from django.db import models
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from Account.managers import CustomUserManager

# Create your models here.

class UserMaster(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200,unique=True)
    email = models.EmailField(max_length=255,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_logged_in=models.BooleanField(default=False)
    profile_picture=models.FileField(upload_to='profile_picture/',null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(blank=True,null=True)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
 
    def __str__(self):
        return self.username

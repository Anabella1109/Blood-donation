from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # is_superuser=models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)
    is_center = models.BooleanField(default=False)


class Donor (models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10,null=True)
    location =models.CharField(max_length=100)

 

class Center(models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10,null=True)
    location =models.CharField(max_length=100)

def get_success_url(self):
     return self.get_object().get_absolute_url()

# Create your models here.

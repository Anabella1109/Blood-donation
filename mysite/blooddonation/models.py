from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from location_field.models.plain import PlainLocationField
# from django.utils.timezone import timezone

class User(AbstractUser):
    # is_superuser=models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)
    is_center = models.BooleanField(default=False)


class Donor (models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    email=models.EmailField(default=False, blank=False)
    CHOICES = (
        ('AP', 'A+'),
        ('AM', 'A-'),
        ('BP', 'B+'),
        ('BM', 'B-'),
        ('ABP', 'AB+'),
        ('ABM', 'AB-'),
        ('OP', 'O+'),
        ('OM', 'O-'),
    )
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    blood_group=models.CharField(max_length=20,choices=CHOICES,default='A+')
    phone_number=PhoneNumberField(default="0700000000")
    location =models.CharField(max_length=100)

 

class Center(models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    email=models.EmailField(default=False, blank=False)
    name=models.CharField(max_length=100,blank=False)
    phone_number=PhoneNumberField(default="0700000000")
    location =location = PlainLocationField(based_fields=['city'], zoom=7)

    @classmethod
    def search_by_name(cls,search_term):
        centers = cls.objects.filter(name__icontains=search_term)
        return centers

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class Profile(models.Model):
        # photo=models.ImageField(upload_to='images/',default='images/avatar.jpg')
        bio=models.TextField()
        user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
        first_name=models.CharField(max_length=100,null=True)
        last_name=models.CharField(max_length=100,null=True)
        phone_number=PhoneNumberField(default="0700000000")
        country=models.CharField(max_length=100,default='unknown',null=True)
    

        def save_profile(self):
            self.save()
        def delete_profile(self):
            self.delete()

        def update_bio(self,bio):
            self.bio=bio
            self.save()
    

        @receiver(post_save, sender=User)
        def update_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)
            instance.profile.save()

    
    
class Appointment(models.Model):
        user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
        center=models.OneToOneField(Center,on_delete=models.CASCADE,null=True)
        first_name=models.CharField(max_length=100,null=True)
        last_name=models.CharField(max_length=100,null=True)
        phone_number=PhoneNumberField(default="0700000000")
        country=models.CharField(max_length=100,default='unknown',null=True)
    
    
class Event(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    repetitive=models.BooleanField()
    starting=models.DateField(null=True)
    ending=models.DateField(null=True)
    start_time=models.TimeField(null=True)
    end_time=models.TimeField(null=True)
    location=models.CharField(max_length=200)

    def save_event(self):
            self.save()
    def delete_event(self):
            self.delete()



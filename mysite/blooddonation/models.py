from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    EMAIL_FIELD=models.EmailField(default=False, blank=False)
    # is_superuser=models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)
    is_center = models.BooleanField(default=False)


class Donor (models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_number=models.IntegerField(max_length=10,null=True)
    location =models.CharField(max_length=100)

 

class Center(models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    name=models.CharField(max_length=100)
    phone_number=models.IntegerField(max_length=10,null=True)
    location =models.CharField(max_length=100)

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
        phone_number=models.IntegerField(null=True)
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

    
    
# class Appointment(models.Model):
#         user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
#         center=models.ChoicesMeta
#         first_name=models.CharField(max_length=100,null=True)
#         last_name=models.CharField(max_length=100,null=True)
#         phone_number=models.IntegerField(null=True)
#         country=models.CharField(max_length=100,default='unknown',null=True)
    
    




# Create your models here.

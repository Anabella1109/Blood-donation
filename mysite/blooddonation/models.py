from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from location_field.models.plain import PlainLocationField
# from notifications.base.models import AbstractNotification
from django.contrib.auth.models import AbstractUser


# from django.utils.timezone import timezone

class User(AbstractUser):
    # is_superuser=models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)
    is_center = models.BooleanField(default=False)


class Donor (models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    email=models.EmailField(default=False, blank=False)
    CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    blood_group=models.CharField(max_length=20,choices=CHOICES,default='A+')
    phone_number=PhoneNumberField(default="0700000000")
    location =models.CharField(max_length=100)

 

class Center(models.Model):
    user=models.OneToOneField(User , on_delete= models.CASCADE, primary_key=True)
    email=models.EmailField(default=False, blank=False)
    name=models.CharField(max_length=100,blank=False,unique=True)
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
        first_name=models.CharField(max_length=100,null=True,default="Edit your first name...")
        last_name=models.CharField(max_length=100,null=True,default="Edit your last name...")
        phone_number=PhoneNumberField(default="0700000000")
        country=models.CharField(max_length=100,default='unknown',null=True)
        instagram=models.CharField(max_length=100,null=True)
        twitter=models.CharField(max_length=100,null=True)
        facebook=models.CharField(max_length=100,null=True)
    

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
        # user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
        CHOIX=(
        ('Whole blood', 'Whole blood'),
        ('Placelet', 'Placelet'),
        ('Power red', 'Power red'),
        ('',''),
          )
        donation_type=models.CharField(max_length=20,choices=CHOIX,default='Whole blood')
        center=models.ForeignKey(Center, on_delete=models.CASCADE, related_name='center',default=None)
        first_name=models.CharField(max_length=100,null=True)
        last_name=models.CharField(max_length=100,null=True)
        email=models.CharField(max_length=100,null=True)
        phone_number=PhoneNumberField(default="0700000000")
        date=models.DateField(null=True)
        time=models.TimeField(null=True)
        location=models.CharField(max_length=100,default='unknown',null=True)
    
    
class Event(models.Model):
    host = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='host',default=None)
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

class Donation(models.Model):
    CHOIX=(
        ('Whole blood', 'Whole blood'),
        ('Placelet', 'Placelet'),
        ('Power red', 'Power red'),
        ('',''),
          )
    donor=models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donor',default=None)
    donation_type=models.CharField(max_length=20,choices=CHOIX,default='Whole blood')
    center=models.ForeignKey(Center, on_delete=models.CASCADE, related_name='centre',default=None)
    datestamp=models.DateTimeField(auto_now_add=True)

# class Notification(AbstractNotification):
#     # custom field example
#     category = models.ForeignKey(Event,
#                                  on_delete=models.CASCADE)

#     class Meta(AbstractNotification.Meta):
#         abstract = False



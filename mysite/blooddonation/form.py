from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Center,Donor, User, Profile
from django import forms


class DonorsSignUpForm(UserCreationForm):
    first_name= forms.CharField(required=True)
    last_name= forms.CharField(required=True)
    phone_number= forms.CharField(required=True)
    location= forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_donor=True
        user.save()
        donor= Donor.objects.create(user=user)
        donor.first_name=self.cleaned_data.get('first_name')
        donor.last_name=self.cleaned_data.get('last_name')
        donor.phone_number=self.cleaned_data.get('phone_number')
        donor.location=self.cleaned_data.get('location')
        donor.save()
        return donor

class CentersSignUpForm(UserCreationForm):
    name= forms.CharField(required=True)
    phone_number= forms.CharField(required=True)
    location= forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model=User    

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_center=True
        user.save()
        center= Center.objects.create(user=user)
        name=self.cleaned_data.get('name')
        center.phone_number=self.cleaned_data.get('phone_number')
        center.location=self.cleaned_data.get('location')
        center.save()
        return center   

class Loginform(forms.ModelForm):
     class Meta:
         model= User
         exclude = []


class Profileform(forms.ModelForm):
     class Meta:
         model= Profile
         exclude = ['user']    
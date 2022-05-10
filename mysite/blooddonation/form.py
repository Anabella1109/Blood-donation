from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Center,Donor, User, Profile, Event,Appointment,Donation
from django import forms
from location_field.forms.plain import PlainLocationField
from phonenumber_field.formfields import PhoneNumberField


class DonorsSignUpForm(UserCreationForm):
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
    email=forms.EmailField(required=True)
    first_name= forms.CharField(required=True)
    last_name= forms.CharField(required=True)
    blood_group=forms.ChoiceField(required=True,choices=CHOICES)
    phone_number= PhoneNumberField(required=True)
    location= forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_donor=True
        user.email=self.cleaned_data.get('email')
        user.save()
        donor= Donor.objects.create(user=user)
        donor.email=self.cleaned_data.get('email')
        donor.first_name=self.cleaned_data.get('first_name')
        donor.last_name=self.cleaned_data.get('last_name')
        donor.blood_group=self.cleaned_data.get('blood_group')
        donor.phone_number=self.cleaned_data.get('phone_number')
        donor.location=self.cleaned_data.get('location')
        donor.save()
        return donor

class CentersSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    name= forms.CharField(required=True)
    phone_number= PhoneNumberField(required=True)
    location= PlainLocationField(based_fields=['city'],
                                  initial='-22.2876834,-49.1607606')
    class Meta(UserCreationForm.Meta):
        model=User    

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_center=True
        user.save()
        center= Center.objects.create(user=user)
        center.email=self.cleaned_data.get('email')
        center.name=self.cleaned_data.get('name')
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

class EventForm(forms.ModelForm):
     class Meta:
         model=Event
         exclude=[]

class DonationForm(forms.ModelForm):
     DONORS=Donor.objects.all()
     
     class Meta:
         model=Event
         exclude=[]


class AppointmentForm(forms.ModelForm):
    CENTERS=Center.objects.all()
    CHOIX=(
        ('Whole blood', 'Whole blood'),
        ('Placelet', 'Placelet'),
        ('Power red', 'Power red'),
        ('',''),
    )
    donation_type=forms.ChoiceField(required=True,choices=CHOIX,label="Choose Type")
    center=forms.ModelChoiceField(required=True,queryset=CENTERS,to_field_name='name',empty_label="Choose center")
    email=forms.EmailField(required=True)
    first_name= forms.CharField(required=True)
    last_name= forms.CharField(required=True)
    phone_number= PhoneNumberField(required=True)
    date=forms.DateField()
    time=forms.TimeField()
    location= forms.CharField(required=True)

    class Meta:
           model=Appointment
           exclude=[]
    
    @transaction.atomic
    def save(self):
        center=self.cleaned_data.get('center')
        appointment=Appointment.objects.create(center=center)
        appointment.donation_type=self.cleaned_data.get('donation_type')
        appointment.center=self.cleaned_data.get('center')
        appointment.email=self.cleaned_data.get('email')
        appointment.first_name=self.cleaned_data.get('first_name')
        appointment.last_name=self.cleaned_data.get('last_name')
        appointment.phone_number=self.cleaned_data.get('phone_number')
        appointment.date=self.cleaned_data.get('date')
        appointment.time=self.cleaned_data.get('time')
        appointment.location=self.cleaned_data.get('location')
        appointment.save()
        return appointment

        
        #    exclude=[]
        
    
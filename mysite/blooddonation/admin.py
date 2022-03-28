from django.contrib import admin
from .models import User,Center, Donor,Event,Profile,Appointment

admin.site.register(User)
admin.site.register(Donor)
admin.site.register(Center)
admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Appointment)


# Register your models here.

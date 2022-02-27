from django.contrib import admin
from .models import User,Center, Donor

admin.site.register(User)
admin.site.register(Donor)
admin.site.register(Center)

# Register your models here.

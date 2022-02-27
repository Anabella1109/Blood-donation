from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Donor, Center, User
from .form import DonorsSignUpForm,CentersSignUpForm,Loginform
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
# from django.core.urlresolvers import reverse


def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request,'../templates/register.html')

def login(request):
    return render(request,'../templates/login.html')

class donor_register(CreateView):
      model= User
      form_class= DonorsSignUpForm
      template_name= '../templates/donor_register.html'
      success_url= reverse_lazy('index')
      success_message= "Account Created"


    #   def get_absolute_url(self):
    #       return reverse('index',kwargs='slug',self.slug)

      def validation(self,form):
          user=form.save()
          login(self.request,user)
          return redirect('')

class center_register(CreateView):
      model= User
      form_class= CentersSignUpForm
      template_name= '../templates/center_register.html'
      success_url= reverse_lazy('index')
      success_message= "Account Created"




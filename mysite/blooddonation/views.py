from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Donor, Center, User, Profile, Event,Appointment
from .form import DonorsSignUpForm,CentersSignUpForm,Loginform,Profileform, EventForm,AppointmentForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,user_logged_in,user_logged_out
from django.core.mail import send_mail,send_mass_mail
from django.test import Client
import random
# from django.contrib import messages

# from django.core.urlresolvers import reverse


def index(request):
    # quiz = Quiz.objects.all()
    # para = {'quiz' : quiz}
    current_user = request.user
    centerss=Center.objects.all()
    centers=random.choices(centerss,k=3)
    return render(request, 'index.html',{'centers':centers,'user':current_user})

def requirements(request):
    return render(request,'../templates/requirements.html')

def register(request):
    return render(request,'../templates/register.html')

def log(request):
    if 'username' in request.POST:
        username = request.POST['username']
    else:
       username = None 

    if 'password' in request.POST:
        password = request.POST['password']
    else:
        password = None 
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'index.html')
        
    else:
        context = {'error': 'Wrong credintials'}  # to display error?
        return render(request, 'login.html', {'context': context})

# def logind(client: Client, user: User) -> None:
#     """
#     Disconnect the update_last_login signal and force_login as `user`
#     Ref: https://stackoverflow.com/questions/38156681/error-about-django-custom-authentication-and-login
#     Args:
#         client: Django Test client instance to be used to login
#         user: User object to be used to login
#     """
#     user_logged_in.disconnect(receiver=update_last_login)
#     client.force_login(user=user)
#     user_logged_in.connect(receiver=update_last_login)
        # Return an 'invalid login' error message.
       
def pagelogout(request):
    logout(request)

    return render(request,'index.html')


def quiz(request):
    return render(request,'../templates/quiz.html')

class donor_register(CreateView):
    model= User
    form_class= DonorsSignUpForm
    template_name= '../templates/donor_register.html'
    success_url= reverse_lazy('index')

    def validation(self,form):
        user=form.save()
        login(self.request,user)
        return redirect('index')

class center_register(CreateView):
    model= User
    form_class= CentersSignUpForm
    template_name= '../templates/center_register.html'
    success_url= reverse_lazy('index')
    success_message= "Account Created"

    def validate(self,form):
        user=form.save()
        login(self.request,user)
        return redirect('index')
    # if request.method== "POST":
	# 	   form= CentersSignUpForm(request.POST)
	# 	   if form.is_valid():
	# 		    user = form.save()
    #             user_logged_in.disconnect(receiver=update_last_login)
    #             client.force_login(user=user)
    #             user_logged_in.connect(receiver=update_last_login)
	# 		    login(request, user)
	# 		    messages.success(request, "Registration successful." )
	# 		    return redirect("index")
	# 	   messages.error(request, "Unsuccessful registration. Invalid information.")
    # form = CentersSignUpForm()
    # return render (request=request, template_name="center_register.html",context={"form":form})
		      
      

class create_event(CreateView):
    model=Event
    form_class= EventForm
    users=User.objects.all()
    i=0
    emails=["a@gmail.com"]*len(users)
    while i < len(users):
        for user in  users:
            emails[i]=user.email
        i+=1

    send_mail("New Event Alert","Dear Donor, A new event that might interest you is happenning. visit Dona at http://127.0.0.1:8000/  for more info","bellaxbx1109@gmail",emails,connection=None)
    template_name='../templates/createevent.html'
    success_url= reverse_lazy('index')

@login_required(login_url='/login/')
def profiles(request,email):
     user=request.user
     profile=Profile.objects.get(user=user)
     donor=Donor.objects.filter(user=user)
     events=Event.objects.all()
     return render(request, 'profile.html',{"email":email,"user":user,"profile": profile,'donor':donor,"events":events})

def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Center.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"centers": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

def events(request):
    events=Event.objects.all()
    return render(request,'events.html', {'events':events})

def cent(request,name):
    center=Center.objects.get(name=name)
    user=User.objects.get(center=center)
    events=Event.objects.filter(host=center)
    return render(request,'center.html',{'center':center,'user':user,'events':events})


@login_required(login_url='login/')
def edit_profile(request,edit):
    current_user = request.user
    profile=Profile.objects.get(user=current_user)
    
   
    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES)
        if form.is_valid():
            
            profile.bio=form.cleaned_data['bio']
            # profile.photo = form.cleaned_data['photo']
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.country = form.cleaned_data['country']
            profile.instagram = form.cleaned_data['instagram']
            profile.twitter = form.cleaned_data['twitter']
            profile.facebook = form.cleaned_data['facebook']
            profile.user=current_user
            
            profile.save_profile()
        return redirect('index')

    else:
        form = Profileform()
    return render(request, 'edit_profile.html', {"form": form , 'user':current_user})

class create_appointment(CreateView):
    model=Appointment
    form_class= AppointmentForm
    # users=User.objects.all()
    # i=0
    # emails=["a@gmail.com"]*len(users)
    # while i < len(users):
    #     for user in  users:
    #         emails[i]=user.email
    #     i+=1

    # send_mail("New Event Alert","Dear Donor, A new event that might interest you is happenning. visit Dona at http://127.0.0.1:8000/  for more info","bellaxbx1109@gmail",emails,connection=None)
    template_name='../templates/appointment.html'
    success_message="Appointment Booked Successully"
    success_url= reverse_lazy('index')


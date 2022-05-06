from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Donor, Center, User, Profile, Event
from .form import DonorsSignUpForm,CentersSignUpForm,Loginform,Profileform, EventForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail,send_mass_mail

# from django.core.urlresolvers import reverse


def index(request):
    # quiz = Quiz.objects.all()
    # para = {'quiz' : quiz}
    centers=Center.objects.all()
    return render(request, 'index.html',{'centers':centers})

def register(request):
    return render(request,'../templates/register.html')

def log(request):
    username = request.POST.get('email',"Bella")
    password = request.POST.get('password',"bellamav")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        success_url= reverse_lazy('index')
        return render(request,'../templates/index.html')
        
    else:
        context = {'error': 'Wrong credintials'}  # to display error?
        return render(request, 'login.html', {'context': context})
        # Return an 'invalid login' error message.
       
def pagelogout(request):
    logout(request)

    return render(request,'index.html')
# def login(request):
#     return render(request,'../templates/login.html')

def quiz(request):
    return render(request,'../templates/quiz.html')

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

    #   send_mass_mail("New Event Alert","Dear Donor, A new event that might interest you is happenning. visit Dona at http://127.0.0.1:8000/  for more info","bellaxbx1109@gmail",emails,connection=None)
      template_name='../templates/createevent.html'
      success_url= reverse_lazy('index')

@login_required(login_url='/login/')
def profiles(request,email):
     user=User.objects.get(email=email)
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
            profile.user=current_user
            
            profile.save_profile()
        return redirect('index')

    else:
        form = Profileform()
    return render(request, 'edit_profile.html', {"form": form , 'user':current_user})
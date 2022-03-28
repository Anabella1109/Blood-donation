from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('donor_register/', views.donor_register.as_view(), name='donor_register'),
    path('center_register/', views.center_register.as_view(), name='center_register'),
    path('quiz/', views.quiz, name='quiz'),
    # path('edit_profile/(\d+)',views.edit_profile,name ='edit_profile') ,
    path('profile/',views.profile,name ='profile') ,
    path('search/', views.search_results, name='search_results'),
    path('create_event/', views.create_event.as_view(), name='create_event'),
    path('events/', views.events, name='events'),
    # path("<int:myid>/", views.quiz, name="quiz"), 
    # path("quiz/", views.quiz, name="quiz"), 
    # path('<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    # path('<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
]
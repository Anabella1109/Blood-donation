from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('requirements/', views.requirements, name='requirements'),
    path('types/', views.types, name='types'),
    path('tips/', views.tips, name='tips'),
    path('login/', views.log, name='login'),
    path('donor_register/', views.donor_register.as_view(), name='donor_register'),
    path('center_register/', views.center_register.as_view(), name='center_register'),
    path('quiz/', views.quiz, name='quiz'),
    path('edit_profile/<str:edit>',views.edit_profile,name ='edit_profile') ,
    path('profiles/<str:email>',views.profiles,name ='profiles') ,
    path('search/', views.search_results, name='search_results'),
    path('create_event/', views.create_event.as_view(), name='create_event'),
    path('appointment/', views.create_appointment.as_view(), name='appointment'),
    path('events/', views.events, name='events'),
    path('center/<str:name>', views.cent, name='center'),
    path('logout/', views.pagelogout, name='logout'),
    # path( "/dashboard",
    #     TemplateView.as_view(template_name="layouts/dashboard.html"),
    #     name="dashboard",),
    # path('accounts/logout/', views.LogoutView.as_view(template_name="post_list.html"), name='logout'),
    # path("<int:myid>/", views.quiz, name="quiz"), 
    # path("quiz/", views.quiz, name="quiz"), 
    # path('<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    # path('<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
]
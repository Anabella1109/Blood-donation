from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('donor_register/', views.donor_register.as_view(), name='donor_register'),
    path('center_register/', views.center_register.as_view(), name='center_register'),
]
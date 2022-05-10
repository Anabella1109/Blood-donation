from django.urls import path

from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chats'),
    path('chat/<str:sender>/<str:receiver>/', views.message_view, name='chat'),
    path('api/messages/&lt;int:sender&gt;/&lt;int:receiver&gt;/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
]
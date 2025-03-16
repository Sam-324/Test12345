from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpage), #this is accessed by http://localhost:8000/
    path('chat/', views.chatpage), #this is accessed by http://localhost:8000/chat
]
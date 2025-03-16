from django.urls import path
from . import views

urlpatterns = [
    path('rpc/', views.getData), #this is accessed by http://localhost:8000/API/rpc/
]
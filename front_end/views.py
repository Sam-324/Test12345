from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def indexpage(request):
    return render(request,'index.html')

def chatpage(request):
    return render(request,'chat.html')
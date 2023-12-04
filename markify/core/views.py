from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')


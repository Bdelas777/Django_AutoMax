from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def landing_page(request):
    return HttpResponse("<h1>Welcome to AutoMax!</h1>")
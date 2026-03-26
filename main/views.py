from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


def main_view(request):
    return render(request, "views/main.html", {"name": "AutoMax"})

def landing_page(request):
    return render(request, 'views/main.html')

@login_required
def home_view(request):
    return render(request, 'views/home.html')
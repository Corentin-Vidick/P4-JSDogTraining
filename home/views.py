from django.shortcuts import render
from django.views import generic, View


def home(request):
    """
    Contact form success confirmation
    """
    return render(request, "home/home.html")

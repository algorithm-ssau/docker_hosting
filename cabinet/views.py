from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    """index.html"""
    return render(request, "cabinet/index.html")

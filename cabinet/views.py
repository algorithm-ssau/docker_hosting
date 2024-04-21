from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
@login_required(login_url='/login')
def index(request):
    """index.html"""
    return render(request, "cabinet/index.html")

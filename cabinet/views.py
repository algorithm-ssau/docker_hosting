from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import CustomUser
from cabinet.models import Billing


# Create your views here.
@login_required(login_url='/login')
def index(request):
    """index.html"""
    return render(request, "cabinet/index.html")


@login_required(login_url='/login')
def profile(request):
    """profile.html"""
    return render(request, "cabinet/profile.html")


@login_required(login_url='/login')
def billing(request):
    """billing.html"""
    user = request.user
    userWallet = user.wallet
    billingsBD = Billing.objects.filter(user=user).all()
    billings = list(billingsBD.values()) # Преобразование в список словарей
    return render(request, "cabinet/billing.html", {'billings': billings, 'userWallet': userWallet})


@login_required(login_url='/login')
def containers(request):
    """containers.html"""
    return render(request, "cabinet/containers.html")

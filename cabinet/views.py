from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import CustomUser
from cabinet.models import Billing, Container, ContainerStats, User_rent_docker


# Create your views here.
@login_required(login_url='/login')
def index(request):
    """index.html"""
    user = request.user
    conts = User_rent_docker.objects.filter(user_id=user.id).all()
    containers = {}
    for cont in conts:
        if cont.container_id in containers:
            containers['cont.container_id'] += list(
                ContainerStats.objects.select_related('container').filter(
                    container_id=cont.container_id).all().values())
        else:
            containers['cont.container_id'] = list(
                ContainerStats.objects.select_related('container').filter(
                    container_id=cont.container_id).all().values())
    return render(request, "cabinet/index.html")


@login_required(login_url='/login')
def profile(request):
    """profile.html"""
    user = request.user
    context = {"username": user.username, "email": user.email, "about_user": user.about_user, "image": user.user_image}
    return render(request, "cabinet/profile.html", context)


@login_required(login_url='/login')
def billing(request):
    """billing.html"""
    user = request.user
    userWallet = user.wallet
    billingsBD = Billing.objects.filter(user=user).all()
    billings = list(billingsBD.values())  # Преобразование в список словарей
    return render(request, "cabinet/billing.html", {'billings': billings, 'userWallet': userWallet})


@login_required(login_url='/login')
def containers(request):
    """containers.html"""
    if request.method == 'POST':
        pass
    user = request.user
    conts = User_rent_docker.objects.filter(user_id=user.id).values()
    # словарь словарей
    containers = {}
    rents = {}
    for cont in conts:
        rent = cont
        container = list(Container.objects.filter(id=cont['container_id']).values())[0]
        containers[cont['container_id']] = rent | container
    return render(request, "cabinet/containers.html", {'containers': containers})

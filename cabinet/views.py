from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
import socket
from .models import CustomUser, Hosting
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
    user = request.user
    conts = User_rent_docker.objects.filter(user_id=user.id).values()
    # словарь словарей
    containers = {}
    rents = {}
    for cont in conts:
        rent = cont
        container = list(Container.objects.filter(id=cont['container_id']).values())[0]
        # получаем hostname по ip
        hosting = list(Hosting.objects.filter(id=container['hosting_id']).values('address'))[0]
        try:
            hosting['address'] = socket.gethostbyaddr(hosting['address'])[0]
        except socket.herror:
            hosting['address'] = "Unknown hostname"
        containers[cont['container_id']] = rent | container | hosting
    exclude_ids = [x['container_id'] for x in list(conts.values('container_id'))] # список всех container_id, принадлежащих user
    available_containers = list(Container.objects.exclude(id__in=exclude_ids).values())
    return render(request, "cabinet/containers.html", {'containers': containers, 'available_containers': available_containers})


@login_required(login_url='/login')
def change_container_status(request):
    if request.method == 'POST':
        container_id = request.POST.get('container_id')
        container_status = request.POST.get('container_status')
        # изменить статус контейнера (true/false)
        Container.objects.filter(id=container_id).update(is_working=container_status)
    # пока просто перебрасывает на пустую страницу контейнеров, еще раз клацнуть на контейнеры для обновления
    return render(request, "cabinet/containers.html")


def change_image_link(request):
    if request.method == 'POST':
        image_link = request.POST.get('image_link')
        container_id = request.POST.get('container_id')
        new_image_link = request.POST.get('new_image_link')
        #проверить линк
    return render(request, "cabinet/containers.html")

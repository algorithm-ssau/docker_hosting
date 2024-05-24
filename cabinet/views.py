from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import redirect
from cabinet.forms import ImageLinkForm
from .models import CustomUser, Hosting
from cabinet.models import Billing, Container, ContainerStats, User_rent_docker, ContainerConfig
from datetime import datetime
from cabinet.task import run_container

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
    if request.method == "POST":
        sum = float(request.POST['sum'])
        user = request.user
        user.wallet += sum
        user.save(update_fields=['wallet'])
        current_datetime = datetime.now()
        bill = Billing.objects.create(done_at=current_datetime, user=user, sum=sum, type='top up')
        bill.save()
        return redirect(reverse('cabinet_billing'))
    else:
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
    hosting = {}
    for cont in conts:
        rent = cont
        container_info = Container.objects.filter(id=cont['container_id'])
        container = list(container_info.values())[0]
        hosting['city'] = container_info.first().hosting.city
        containers[cont['container_id']] = rent | container | hosting

    # необходимо исключить id контейнеров, находящихся в пользовании другими юзерами
    #exclude_ids = [x['container_id'] for x in
                  # list(conts.values('container_id'))]  # список всех container_id, принадлежащих user
    #available_containers = list(
        #Container.objects.exclude(id__in=exclude_ids).values('cores', 'cost', 'disk_space', 'memory_space', 'id'))

    available_containers = list(ContainerConfig.objects.all().values('cores', 'cost', 'disk_space', 'memory_space', 'id'))
    
    errors = []
    validation_errors = {}
    return render(request, "cabinet/containers.html", {'containers': containers,
                                                       'available_containers': available_containers, 'errors': errors,
                                                       'validation_errors': validation_errors})


@login_required(login_url='/login')
def change_container_status(request):
    """containers.html"""
    if request.method == 'POST':
        container_id = request.POST.get('container_id')
        container_status = request.POST.get('container_status')
        # изменить статус контейнера (true/false), проверив, что такой контейнер есть у юзера и он оплачен
        if (User_rent_docker.objects.filter(user_id=request.user.id, container_id=container_id, pay=True).exists()):
            Container.objects.filter(id=container_id).update(is_working=container_status)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def change_image_link(request):
    """containers.html"""
    if request.method == 'POST':
        container_id = request.POST.get('container_id_image')
        new_image_link = request.POST.get('new_link')
        container_form = ImageLinkForm(request.POST)
        if not container_form.is_valid():
            validation_errors = {"validation_errors": container_form.errors}
            return redirect(request.META.get('HTTP_REFERER'))
        if (User_rent_docker.objects.filter(user_id=request.user.id,
                                            container_id=container_id,
                                            pay=True).exists()):  # контейнер принадлежит юзеру и оплачен
            if (True):
                # проверить нормальность линка на докерхаб
                container = Container.objects.get(id=container_id)
                container.docker_image_link = new_image_link
                container.save(update_fields=["docker_image_link"])
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                errors = ["New image link is not valid"]
                return redirect(request.META.get('HTTP_REFERER'))  #
        else:
            errors = ["User doesn't have access to this container"]
            return redirect(request.META.get('HTTP_REFERER'))  #
    return redirect(request.META.get('HTTP_REFERER'))  #


@login_required(login_url='/login')
def buy_new_container(request):
    """containers.html"""
    if request.method == "POST":
        container_form = ImageLinkForm(request.POST)
        if not container_form.is_valid():
            context = {"validation_errors": container_form.errors}
            # необходимо добавить id, ссылку
        req = request.POST
        cont_id = request.POST.get('selected_container_id')
        image = request.POST.get('docker_image_link')
        cost = ContainerConfig.objects.get(id=cont_id).cost
        if (request.user.wallet < cost):
            # ошибка, недостаточно средств на счете
            pass
        if (False):
            pass
            # проверить валидность ссылки docker контейнера
        # пройдены все проверки
        user = request.user.id
        print(run_container.delay(user, cont_id, image))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def telemetry(request):
    """containers.html"""
    return render(request, "cabinet/telemetry.html")

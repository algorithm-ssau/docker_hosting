from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import redirect
from cabinet.forms import ImageLinkForm, ConfigLinkForm
from .models import CustomUser, Hosting
from cabinet.models import Billing, Container, ContainerStats, User_rent_docker, ContainerConfig
from datetime import datetime
from cabinet.task import run_container, stop_container, start_container, pull_image, get_container_logs, update_container_image, change_container_working_status

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

    available_configs = list(ContainerConfig.objects.all().values('cores', 'cost', 'disk_space', 'memory_space', 'id'))
    errors = []
    validation_errors = {}
    return render(request, "cabinet/containers.html", {'containers': containers,
                                                       'available_configs': available_configs, 'errors': errors,
                                                       'validation_errors': validation_errors})


@login_required(login_url='/login')
def change_container_status(request):
    """containers.html"""
    if request.method == 'POST':
        container_id = request.POST.get('container_id')
        if (User_rent_docker.objects.filter(user_id=request.user.id, container_id=container_id, pay=True).exists()):
            change_container_working_status.delay(container_id)
        else:
            # ошибка контейнер не оплачен
            return redirect(request.META.get('HTTP_REFERER'))
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
        if not User_rent_docker.objects.filter(user_id=request.user.id, container_id=container_id, pay=True).exists():
            error = [""] #ошибка не оплачен у пользователя
            return redirect(request.META.get('HTTP_REFERER'))
        e = update_container_image.delay(container_id, new_image_link)
        if(e):
            return redirect(request.META.get('HTTP_REFERER'))
            # ошибка невалидный образ (или что-то еще)))))
    return redirect(request.META.get('HTTP_REFERER'))  


@login_required(login_url='/login')
def buy_new_container(request):
    """containers.html"""
    if request.method == "POST":
        container_form = ConfigLinkForm(request.POST)
        if not container_form.is_valid():
            context = {"validation_errors": container_form.errors}
            # необходимо добавить id, ссылку
            return redirect(request.META.get('HTTP_REFERER'))
        cont_id = request.POST.get('selected_config_id')
        image = request.POST.get('docker_image_link')
        cost = ContainerConfig.objects.get(id=cont_id).cost
        if (request.user.wallet < cost):
            # ошибка, недостаточно средств на счете
            return redirect(request.META.get('HTTP_REFERER'))
        user = request.user.id
        run_container.delay(user, cont_id, image)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def telemetry(request):
    """containers.html"""
    return render(request, "cabinet/telemetry.html")

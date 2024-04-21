from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

from cabinet.models import CustomUser
from index_app.forms import UserRegisterForm
from index_app.forms import UserLoginForm

# Create your views here.
def index(request):
    """index.html"""
    return render(request, "index_app/index.html")


def register_user(request):
    """registration.html"""
    if request.method == 'POST':
        userform = UserRegisterForm(request.POST)
        if not userform.is_valid():
            return render(request, 'index_app/registration.html', context={"validation_errors": userform.errors})
        email = request.POST['email']
        new_username = request.POST['username']
        new_password = request.POST['password']
        user = authenticate(request, username=new_username, password=new_password)
        #CustomUser.objects.
        if user is None:
            count_name = CustomUser.objects.filter(username=new_username).count()
            if count_name != 0:
                return render(request, 'index_app/registration.html', context={"errors":["User with this username already exists."]})
            count_email = CustomUser.objects.filter(email=email).count()
            if count_email != 0:
                return render(request, 'index_app/registration.html', context={"errors": ["User with this email already exists."]})
            # Создание нового пользователя
            new_user = CustomUser.objects.create_user(email=email, username=new_username, password=new_password)
            login(request, new_user)
            # Перенаправление на страницу успеха.
            return redirect(reverse('cabinet_index'))
        else:
            # Возврат сообщения об ошибке "такой пользователь существует".

            return render(request, 'index_app/registration.html', context={"errors":
                ["User with this name already exists."]
            })
    else:
        # Отображение формы входа.
        return render(request, "index_app/registration.html")


def login_user(request):
    """login.html"""
    if request.method == 'POST':
        userform = UserLoginForm(request.POST)
        if not userform.is_valid():
            return render(request, 'index_app/login.html', context={"errors": userform.errors})
        username = request.POST['username']
        user_password = request.POST['password']
        user = authenticate(request, username=username, password=user_password)
        if user is not None:
            login(request, user)
            # Перенаправление на страницу успеха.
            return redirect(reverse('cabinet_index'))
        else:
            # Возврат сообщения об ошибке "неверный логин".
            return render(request, 'index_app/login.html', context={"errors":["User with this name does not exist."]})
    else:
        return render(request, "index_app/login.html")




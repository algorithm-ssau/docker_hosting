from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

from cabinet.models import CustomUser
from index_app.forms import UserRegisterForm


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
        if user is None:
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
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправление на страницу успеха.
            return redirect(reverse('cabinet_index'))
        else:
            # Возврат сообщения об ошибке "неверный логин".
            return render(request, 'invalid_login.html')
    else:
        return render(request, "index_app/login.html")




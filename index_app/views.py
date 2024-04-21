from django.shortcuts import render
from django.contrib.auth import authenticate, login
from cabinet.models import CustomUser

# Create your views here.
def index(request):
    """index.html"""
    return render(request, "index_app/index.html")

def registration(request):
    """registration.html"""
    if request.method == 'POST':
        new_username = request.POST['username']
        new_password = request.POST['password']
        user = authenticate(request, username=new_username, password=new_password)
        if user is None:
            # Создание нового пользователя
            new_user = CustomUser.objects.create_user(username=new_username, password=new_password)
            # Перенаправление на страницу успеха.
            return redirect('cabinet/index.html')
        else:
            # Возврат сообщения об ошибке "такой пользователь существует".
            return render(request, 'invalid_registration.html')
    else:
        # Отображение формы входа.
        return render(request, "index_app/registration.html")
    

def login(request):
    """login.html"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправление на страницу успеха.
            return redirect('cabinet/index.html')
        else:
            # Возврат сообщения об ошибке "неверный логин".
            return render(request, 'invalid_login.html')
    else:
        return render(request, "index_app/login.html")

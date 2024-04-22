from django.contrib import admin
from django.urls import path, include
from index_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
]

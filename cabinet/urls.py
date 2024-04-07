from django.contrib import admin
from django.urls import path, include
from cabinet import views

urlpatterns = [
    path('', views.index),
]
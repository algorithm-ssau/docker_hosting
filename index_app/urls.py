from django.contrib import admin
from django.urls import path, include
from index_app import views

urlpatterns = [
    path('', views.index),
    path('registration/', views.registration),
]

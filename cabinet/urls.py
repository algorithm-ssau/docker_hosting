from django.contrib import admin
from django.urls import path, include
from cabinet import views

urlpatterns = [
    path('', views.index, name='cabinet_index'),
    path('profile/', views.profile, name='cabinet_profile'),
    path('billing/', views.billing, name='cabinet_billing'),
    path('containers/', views.containers, name='cabinet_containers'),
    path('containers/#', views.change_container_status, name='change_container_status'),
    path('containers/#', views.change_image_link, name='change_image_link'),
]

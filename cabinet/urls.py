from django.contrib import admin
from django.urls import path, include
from cabinet import views

urlpatterns = [
    path('', views.index, name='cabinet_index'),
    path('profile/', views.profile, name='cabinet_profile'),
    path('billing/', views.billing, name='cabinet_billing'),
    path('containers/', views.containers, name='cabinet_containers'),
    path('change_container_status/', views.change_container_status, name='change_container_status'),
    path('change_image_status/', views.change_image_link, name='change_image_link'),
    path('buy_new_container/', views.buy_new_container, name='buy_new_container'),
]

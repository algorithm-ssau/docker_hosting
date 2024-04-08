from django.contrib import admin

# Register your models here.

from .models import Hosting, Container, user_rent_docker

admin.site.register(Hosting) #модель стала доступна на странице администрирования
admin.site.register(Container)
admin.site.register(user_rent_docker)
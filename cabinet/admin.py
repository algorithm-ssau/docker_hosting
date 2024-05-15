from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from .models import Hosting, Container, User_rent_docker, Billing, ContainerStats, ContainerConfig
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('about_user', 'user_image', 'wallet')}),)


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Hosting)  # модель стала доступна на странице администрирования
admin.site.register(Container)
admin.site.register(User_rent_docker)
admin.site.register(Billing)
admin.site.register(ContainerStats)
admin.site.register(ContainerConfig)

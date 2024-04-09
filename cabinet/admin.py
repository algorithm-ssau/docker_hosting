from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from .models import Hosting, Container, user_rent_docker
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('about_user', 'user_image')}), )

    
# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Hosting) #модель стала доступна на странице администрирования
admin.site.register(Container)
admin.site.register(user_rent_docker)
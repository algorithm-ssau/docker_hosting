from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'about_user', 'user_image', 'wallet')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'about_user', 'user_image', 'wallet')


class ConfigLinkForm(forms.Form):
    docker_image_link = forms.CharField(required=True, min_length=2)
    selected_config_id = forms.CharField(required=True, min_length=1)

class ImageLinkForm(forms.Form):
    new_link = forms.CharField(required=True, min_length=2)
    container_id_image = forms.CharField(required=True, min_length=1)
from django import forms


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=2, max_length=20)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=2, max_length=20)

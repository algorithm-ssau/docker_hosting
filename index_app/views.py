from django.shortcuts import render


# Create your views here.
def index(request):
    """login.html"""
    return render(request, "index_app/login.html")

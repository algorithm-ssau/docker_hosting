from django.shortcuts import render


# Create your views here.
def index(request):
    """index.html"""
    return render(request, "index_app/index.html")

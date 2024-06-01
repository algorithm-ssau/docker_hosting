from django.urls import path
from .consumers import DockerConsumer

ws_urlpatterns=[
    path('ws/cabinet/', DockerConsumer.as_asgi())
]
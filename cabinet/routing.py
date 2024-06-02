from django.urls import path, re_path
from .consumers import DockerConsumer

ws_urlpatterns=[
    re_path(r'ws/cabinet/$', DockerConsumer.as_asgi())
]
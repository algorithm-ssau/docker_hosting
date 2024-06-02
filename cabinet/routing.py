from django.urls import path, re_path
from .consumers import DockerConsumer, LogsConsumer

ws_urlpatterns=[
    re_path(r'ws/cabinet/$', DockerConsumer.as_asgi()),
    re_path(r'ws/containers/$', LogsConsumer.as_asgi()),
]
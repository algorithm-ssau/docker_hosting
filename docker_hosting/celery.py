import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker_hosting.settings")
app = Celery("docker_hosting") 
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
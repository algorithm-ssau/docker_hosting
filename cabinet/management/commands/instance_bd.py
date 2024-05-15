from ...models import ContainerConfig, Hosting
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Instance basic container configs and hosting'

    def handle(self, *args, **kwargs):
        hosting_instance = Hosting(port = 8000, cores = 24, address = '127.0.0.1:8000', disk_space = 600, memory_space = 600)
        hosting_instance.save()
        instance1 = ContainerConfig(cores=4, disk_space=500, memory_space=8, cost=100.0, hosting=hosting_instance)
        instance1.save()
        instance2 = ContainerConfig(cores=5, disk_space=500, memory_space=8, cost=120.0, hosting=hosting_instance)
        instance2.save()
        instance3 = ContainerConfig(cores=10, disk_space=500, memory_space=8, cost=500.0, hosting=hosting_instance)
        instance3.save()
        self.stdout.write('done')


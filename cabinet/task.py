from celery import shared_task
import docker
from datetime import datetime, timedelta
from cabinet.models import Container, ContainerStats, User_rent_docker, CustomUser, Billing, ContainerConfig
from django.utils import timezone

@shared_task
def run_container(user_id, cont_id, image):
    try:
        client = docker.from_env()
        container = client.containers.run(image, detach=True)
        container.start()
        print('container_run')
    
        cost = ContainerConfig.objects.get(id=cont_id).cost
        core = ContainerConfig.objects.get(id=cont_id).cores
        disk = ContainerConfig.objects.get(id=cont_id).disk_space
        memory = ContainerConfig.objects.get(id=cont_id).memory_space
        host = ContainerConfig.objects.get(id=cont_id).hosting
    
        user = CustomUser.objects.get(id = user_id)
        #списать со счета
        user.wallet -= cost
        user.save(update_fields=["wallet"])
    
        #создать объект покупки 
        current_datetime = datetime.now()
        bill = Billing.objects.create(done_at=current_datetime, user=user, sum=-cost, type='debite')
        bill.save()
    
        #добавить его в таблицу container 
        container_bd = Container(id = container.id, 
                             docker_image_link = image, 
                             docker_container_link =  container.name,
                             cores = core,
                             disk_space = disk,
                             memory_space = memory,
                             is_working = True,
                             cost = cost,
                             hosting = host)
        container_bd.save()
        date = datetime.today()
        end_date = date + timedelta(days=30)
        #добавить связь с юзером 
        rent = User_rent_docker(user = user,
                            container = container_bd, 
                            start_date = date,
                            end_date = end_date,
                            cost = cost, 
                            pay = True)
        rent.save()
        print('bd complited')
    except Exception as e:
        print(e)
    finally:
        return 'task done'
        
import logging
logger = logging.getLogger()
import requests

@shared_task
def get_stats():
    logger.info('task start')
    print('stats get')
    client = docker.from_env()
    containers = Container.objects.all()
    # для всех запущенных контейнеров собираем статистику
    for db_container in containers:
        container = client.containers.get(db_container.id)

        if container.status == 'exited':
            new_record = ContainerStats.objects.create(
            container=db_container,
            time=timezone.now(),
            cpu=0,
            ram=0,
            disk=0,
            )
            new_record.save()
            continue

        # stats
        stats = container.stats(stream=False)
        name = stats['name']  # 'name': '/UbuntuContainer',
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        number_of_cores = stats['cpu_stats']['online_cpus']
        cpu_percent = (cpu_delta / system_delta) * number_of_cores * 100.0
        time = stats['read']  # 'read': '2024-05-06T10:12:00.461046383Z'
        date_string, microseconds_string = time.split('.')
        # Only keep the first 6 digits of the microseconds
        microseconds_string = microseconds_string[:6]
        # Combine them back
        adjusted_date_string = f"{date_string}.{microseconds_string}Z"
        # Now parse the string with the adjusted format
        your_datetime = datetime.strptime(adjusted_date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        # your_datetime = timezone.make_aware(your_datetime, timezone.utc)
        memory_usage = stats['memory_stats']['usage']  # 'usage': 897024
        # storage_stats = stats['storage_stats']['']  # legacy
        # create a new record to bd
        new_record = ContainerStats.objects.create(
            container=db_container,
            time=your_datetime,
            cpu=cpu_percent,
            ram=memory_usage/1024/1024,
            disk=0,
                # disk=storage_stats
            )
        telemetry=db_container.id
    #     async_to_sync(channel_layer.group_send)(
    #         "group_name", {"type": "container.telemetry", "telemetry": json.dumps({telemetry})}
    # )  
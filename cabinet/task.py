from celery import shared_task
import docker
from datetime import datetime, timedelta
from cabinet.models import Container, User_rent_docker, CustomUser, Billing, ContainerConfig, ContainerStats
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
import requests
import json
from django.utils import timezone
from django.db import transaction

print('container_run')
@shared_task
def run_container(user_id, cont_id, image):
    print("task")
    try:
        client = docker.from_env()
        pull_image(image)
        container = client.containers.run(image, detach=True)
        container.start()
        print('container_run')
    
        cost = ContainerConfig.objects.get(id=cont_id).cost
        core = ContainerConfig.objects.get(id=cont_id).cores
        disk = ContainerConfig.objects.get(id=cont_id).disk_space
        memory = ContainerConfig.objects.get(id=cont_id).memory_space
        host = ContainerConfig.objects.get(id=cont_id).hosting

        date = datetime.today()
        end_date = date + timedelta(days=30)

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
                            is_working = True if container.status == 'running' else False,
                            cost = cost,
                            hosting = host)
        container_bd.save()

        #добавить связь с юзером 
        rent = User_rent_docker(user = user,
                            container = container_bd, 
                            start_date = date,
                            end_date = end_date,
                            cost = cost, 
                            pay = True)
        rent.save()
        print('bd complited')
        while(True):
            get_container_logs.delay(container.id)
    except Exception as e:
        print(e)
    finally:
        return 'task done'
        
import logging
logger = logging.getLogger()
import requests

@shared_task
def get_stats():
    channel_layer = get_channel_layer()
    logger.info('task start')
    print('stats get')
    client = docker.from_env()
    containers = Container.objects.all()
    info = []
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
        info.append({
            "container_id" : db_container.id,
            "cpu_percent": new_record.cpu,
            "ram": new_record.ram,
            "disk": new_record.disk
        })

    async_to_sync(channel_layer.group_send)(
        "docker", {"type": "container.telemetry", "telemetry": json.dumps(info)}
    )

@shared_task
def start_container(cont_id):
    try:
        client = docker.from_env()
        container = client.containers.get(cont_id)
        container.start() ## 
        cont = Container.objects.get(id=cont_id)
        cont.is_working = True if container.status == 'running' else False
        cont.save(update_fields=["is_working"])
        print('start_container done')
    except Exception as e:
        print(e)


@shared_task
def stop_container(cont_id):
    try:
        client = docker.from_env()
        container = client.containers.get(cont_id)
        container.stop()
        cont = Container.objects.get(id=cont_id)
        cont.is_working = True if container.status == 'running' else False
        cont.save(update_fields=["is_working"])
        print('stop_container done')
    except Exception as e:
        print(e)


@shared_task
def update_container_image(container_id, image_name):
    try:
        pull_image(image_name)
         # проверяем существование образа
        client = docker.from_env()
        old_container = client.containers.get(container_id)
        old_container.stop()
        old_container.remove() # удаляем старый контейнер

        new_container = client.containers.run(image_name, name=old_container.name, detach=True) # запускаем новый контейнер с новым образом
        new_container_id = new_container.id 

        old_container = Container.objects.get(id=container_id) # заменяем старые записи о контейнере новыми
        with transaction.atomic():
            new_container = Container.objects.create(
                id=new_container_id,
                docker_image_link= image_name,
                docker_container_link=old_container.docker_container_link,
                login=old_container.login,
                password=old_container.password,
                cores=old_container.cores,
                port=old_container.port,
                disk_space=old_container.disk_space,
                memory_space=old_container.memory_space,
                is_working=True if new_container.status == 'running' else False,
                cost=old_container.cost,
                hosting=old_container.hosting,
            )
            user_rent_records = User_rent_docker.objects.filter(container=old_container)
            for record in user_rent_records:
                record.container = new_container
                record.save()
            old_container.delete()

        get_container_logs.delay(new_container_id)
    except Exception as e:
        print(e)
        return e
        

    
@shared_task
def pull_image(image):
    try:
        client = docker.from_env()
        client.images.pull(image)
    except:
        print('not valid image link')
        raise Exception("Not valid docker image link")

@shared_task
def change_container_working_status(container_id):
    try:
        condition = Container.objects.get(id=container_id).is_working
        if condition:
            stop_container.delay(container_id)
        else:
            start_container.delay(container_id)
    except Exception as e:
        print(e)


@shared_task
def get_container_logs(container_id):
    try:
        client = docker.from_env()
        print('logs find')
        container = client.containers.get(container_id)
        for line in container.logs(follow=True, stream=True):
           logger.info(line.decode('utf-8').strip()) 
           print(line.decode('utf-8').strip())
    except Exception as e:
        print(e)

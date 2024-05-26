from celery import shared_task
import docker
from datetime import datetime, timedelta
from cabinet.models import Container, User_rent_docker, CustomUser, Billing, ContainerConfig
from django.db import transaction

@shared_task
def run_container(user_id, cont_id, image):
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
    except Exception as e:
        print(e)
    finally:
        return 'task done'
        

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
        container = client.containers.get(container_id)
        return container.logs()
    except Exception as e:
        print(e)

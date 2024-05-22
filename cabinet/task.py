from celery import shared_task
import docker
from datetime import datetime, timedelta
from cabinet.models import Container, User_rent_docker, CustomUser, Billing, ContainerConfig

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
        

    
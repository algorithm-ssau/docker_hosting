from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Hosting(models.Model):
    """Хостинг"""

    # Поля
    id = models.AutoField(primary_key=True)
    port =  models.IntegerField()
    cores = models.IntegerField()
    address = models.TextField()
    disk_space =models.IntegerField()
    memory_space = models.IntegerField()

    # Метаданные
    class Meta:
        ordering = ['id']

    # Methods
    #можно прописывать логику типо счета к оплате
    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return self.id +"hosting"
    
class Container(models.Model):
    """Контейнер """

    # Поля
    id = models.AutoField(primary_key=True)
    docker_image_link = models.CharField(max_length=200)
    docker_container_link = models.CharField(max_length=200)
    login = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    cores = models.IntegerField()
    port = models.IntegerField()
    disk_space = models.IntegerField()
    memory_space =  models.IntegerField()
    hosting = models.ForeignKey(
        Hosting,
        on_delete=models.CASCADE,
    )

    # Метаданные
    class Meta:
        ordering = ['id']

    # Methods
    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return self.id+'container'
    
class user_rent_docker(models.Model):
    """Пользователь арендовал докер """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    pay = models.BooleanField()
    cost = models.IntegerField()
    # Метаданные
    class Meta:
        ordering = ['user', 'container']

    # Methods
    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return user.str() + container.str()
    
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.

class CustomUser(AbstractUser):
    """пользователь"""

    # Поля
    about_user = models.CharField(max_length=200)
    user_image = models.CharField(max_length=200)
    wallet = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.username)


class Hosting(models.Model):
    """Хостинг"""

    # Поля
    id = models.AutoField(primary_key=True)
    port = models.IntegerField()
    cores = models.IntegerField()
    address = models.TextField()
    disk_space = models.IntegerField()
    memory_space = models.IntegerField()

    # Метаданные
    class Meta:
        ordering = ['id']

    # Methods
    # можно прописывать логику типо счета к оплате
    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return str(self.id) + "hosting"


class Container(models.Model):
    """Контейнер """

    # Поля
    id = models.AutoField(primary_key=True)
    docker_image_link = models.CharField(max_length=200, blank=True, null=True)
    docker_container_link = models.CharField(max_length=200, blank=True, null=True)
    login = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    cores = models.IntegerField()
    port = models.IntegerField()
    disk_space = models.IntegerField()
    memory_space = models.IntegerField()
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
        return str(self.id) + 'container'


class User_rent_docker(models.Model):
    """Пользователь арендовал докер """
    user = models.ForeignKey(
        CustomUser,
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
        unique_together = ['user', 'container']
        ordering = ['user', 'container']

    # Methods
    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.user) + str(self.container)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return str(self.user.id) + 'user' + str(self.container.id) + 'container'


class Billing(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    done_at = models.DateTimeField(null=False, blank=False)
    sum = models.IntegerField()
    type = models.CharField(max_length=20)

    class Meta:
        unique_together = ['user', 'done_at']
        ordering = ['user', 'done_at']

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.user) + str(self.done_at)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return str(self.user.id) + '_user_done_pay_at_' + str(self.done_at)


class ContainerStats(models.Model):
    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
    )
    time = models.DateField(null=False, blank=False)
    cpu = models.IntegerField()
    ram = models.IntegerField()
    disk = models.IntegerField()

    class Meta:
        unique_together = ['container', 'time']
        ordering = ['container', 'time']

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.container.id) + str(self.time)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return 'Container_' + str(self.container.id) + 'InTime_' + str(self.time)

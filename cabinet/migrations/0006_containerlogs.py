# Generated by Django 5.0.4 on 2024-06-02 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0005_alter_container_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('container', models.IntegerField()),
                ('logs', models.TextField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]

# Generated by Django 5.0.4 on 2024-05-08 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='is_working',
            field=models.BooleanField(default=False),
        ),
    ]
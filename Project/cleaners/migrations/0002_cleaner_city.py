# Generated by Django 3.0 on 2021-08-09 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleaner',
            name='city',
            field=models.CharField(default='Не указан', max_length=100),
        ),
    ]

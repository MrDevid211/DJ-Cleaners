# Generated by Django 3.0 on 2021-08-12 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaners', '0002_auto_20210811_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleaner',
            name='phone_number',
            field=models.CharField(default='None', max_length=50),
        ),
    ]

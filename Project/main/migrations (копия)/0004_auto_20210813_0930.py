# Generated by Django 3.0 on 2021-08-13 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210812_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='duration',
            field=models.IntegerField(default=1),
        ),
    ]

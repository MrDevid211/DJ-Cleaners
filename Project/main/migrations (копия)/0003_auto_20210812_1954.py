# Generated by Django 3.0 on 2021-08-12 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210812_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='cleaner_id',
            field=models.IntegerField(default=0),
        ),
    ]

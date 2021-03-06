# Generated by Django 3.0 on 2021-08-13 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='quality_score',
        ),
        migrations.AddField(
            model_name='booking',
            name='cleaners_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_phone_number',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='booking',
            name='duration',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='unix_time_end',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='booking',
            name='unix_time_start',
            field=models.IntegerField(default=2),
        ),
    ]

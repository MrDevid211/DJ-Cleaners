# Generated by Django 3.2.6 on 2021-08-14 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_rename_booking_booking2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking2',
            name='cleaner',
        ),
        migrations.RemoveField(
            model_name='booking2',
            name='customer',
        ),
    ]

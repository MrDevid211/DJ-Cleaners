# Generated by Django 3.2.6 on 2021-08-14 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20210812_1511'),
        ('cleaners', '0007_auto_20210813_0932'),
        ('bookings', '0002_remove_booking_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Booking',
            new_name='Booking2',
        ),
    ]

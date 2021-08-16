from django.db import models



class Booking(models.Model):
    customer_phone_number = models.CharField(max_length=50, default=0)
    top_cleaners_id = models.IntegerField(default=0)
    city = models.CharField(max_length=100, default='')
    top_cleaners_durations = models.IntegerField(default=1)
    price = models.CharField(max_length=100)

    unix_time_start = models.IntegerField(default=2)
    unix_time_end = models.IntegerField(default=3)


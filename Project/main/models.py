from django.db import models



class Booking(models.Model):
    customer_phone_number = models.CharField(max_length=50)
    cleaner_id = models.IntegerField(default='')
    duration = models.IntegerField(default='')
    date = models.DateField()
    time = models.TimeField()


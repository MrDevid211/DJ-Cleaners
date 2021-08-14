from django.db import models

class CityList(models.Model):
    city = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=100, blank=True)


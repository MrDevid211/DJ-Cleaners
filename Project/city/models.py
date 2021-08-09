from django.db import models

class City(models.Model):
    city = models.CharField(max_length=100, default="")
    other_city = models.CharField(max_length=1001, default="")


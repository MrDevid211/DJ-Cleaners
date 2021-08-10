from django.db import models

class Cleaner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2)
    city = models.CharField(max_length=100, default="")
    other_city = models.CharField(max_length=100, default="")
    duration = models.IntegerField(default="Не указано")


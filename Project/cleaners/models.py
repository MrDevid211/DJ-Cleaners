from django.db import models

class Cleaner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField(default='')
    phone_number = models.CharField(max_length=50, default="")

    city = models.CharField(max_length=100, default="1")
    other_city = models.CharField(max_length=9999, default="2")
    # Костыль для более красивого вывода обслуживаемых городов
    other_city_for_details = models.CharField(max_length=9999, default="3")


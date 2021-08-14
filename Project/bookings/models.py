from django.db import models

from customers.models import Customer
from cleaners.models import Cleaner

class Booking2(models.Model):
    pass
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE) # Добавил для исправления ошибки при запуске
    #cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE) # Добавил для исправления ошибки при запуске

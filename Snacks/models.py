from django.db import models

# Create your models here.


class Snack(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    available = models.BooleanField(default=False)

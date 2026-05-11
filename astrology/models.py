from django.db import models

# Create your models here.
from django.db import models

class Astrologer(models.Model):
    name = models.CharField(max_length=100)
    price_per_min = models.FloatField()
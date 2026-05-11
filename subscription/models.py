from django.db import models

# Create your models here.
from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    days_from = models.IntegerField()
    days_to = models.IntegerField()
    price = models.IntegerField()
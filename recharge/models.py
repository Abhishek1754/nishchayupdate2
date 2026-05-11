from django.db import models

# Create your models here.
from django.db import models

class Recharge(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    amount = models.FloatField()
    cashback = models.FloatField()
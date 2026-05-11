from django.db import models

# Create your models here.
from django.db import models

class WalletTransaction(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    amount = models.FloatField()
    type = models.CharField(max_length=10)
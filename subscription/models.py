
from django.db import models
from django.conf import settings


class SubscriptionPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reward_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2
    )

    reward_coin = models.IntegerField(
        default=10
    )

    validity_days = models.IntegerField(
        default=365
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.name


class UserSubscription(models.Model):

    STATUS_CHOICES = (

        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),

    )

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE

    )

    plan = models.ForeignKey(

        SubscriptionPlan,

        on_delete=models.CASCADE

    )

    amount = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    start_date = models.DateTimeField(

        auto_now_add=True

    )

    expiry_date = models.DateTimeField()

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='ACTIVE'

    )

    def __str__(self):

        return f"{self.user.email} - {self.plan.name}"

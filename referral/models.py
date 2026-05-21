from django.db import models
from accounts.models import User


class ReferralIncome(models.Model):

    INCOME_TYPES = (

        ('roi', 'ROI'),

        ('recharge', 'Recharge'),

        ('ecommerce', 'Ecommerce'),

        ('food', 'Food'),

    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='income_from_user'
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='income_to_user'
    )

    income_type = models.CharField(
        max_length=20,
        choices=INCOME_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.to_user.email} earned {self.amount}"
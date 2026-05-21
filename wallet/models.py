from django.db import models
from accounts.models import User


class WalletTransaction(models.Model):

    TRANSACTION_TYPES = (

        ('credit', 'Credit'),
        ('debit', 'Debit'),

    )

    SOURCE_TYPES = (

        ('roi', 'ROI'),
        ('recharge', 'Recharge'),
        ('ecommerce', 'Ecommerce'),
        ('referral', 'Referral'),
        ('withdraw', 'Withdraw'),
        ('bonus', 'Bonus'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCE_TYPES,
        default='bonus'
    )

    balance_after = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    remark = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.amount}"
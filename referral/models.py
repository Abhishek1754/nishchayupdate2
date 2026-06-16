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


# =========================
# SMART SHARE SETTINGS
# =========================

class SmartShareSetting(models.Model):

    PLAN_TYPES = (

        ('free', 'Free'),
        ('paid', 'Paid'),

    )

    LEVEL_CHOICES = (

        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
        (5, 'Level 5'),

    )

    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPES
    )

    level = models.IntegerField(
        choices=LEVEL_CHOICES
    )

    rupee_reward = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    coin_reward = models.IntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return f"{self.plan_type} Level {self.level}"


# =========================
# SMART SHARE TRANSACTION
# =========================

class SmartShareTransaction(models.Model):

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='smartshare_receiver'
    )

    trigger_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='smartshare_trigger'
    )

    level = models.IntegerField()

    rupee_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    coin_amount = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.receiver.email} Level {self.level}"
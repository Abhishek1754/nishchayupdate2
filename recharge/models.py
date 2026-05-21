from django.db import models

from accounts.models import User


# =========================
# RECHARGE PROVIDER
# =========================

class RechargeProvider(models.Model):

    SERVICE_TYPES = (

        ('mobile', 'Mobile'),
        ('dth', 'DTH'),
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('water', 'Water'),

    )

    name = models.CharField(
        max_length=100
    )

    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPES
    )

    cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    # LEVEL INCOME SETTINGS

    total_levels = models.IntegerField(
        default=1
    )

    level_1_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    level_2_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    level_3_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================
# RECHARGE TRANSACTION
# =========================

class Recharge(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    provider = models.ForeignKey(
        RechargeProvider,
        on_delete=models.CASCADE
    )

    mobile_number = models.CharField(
        max_length=20
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    cashback = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    api_response = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.mobile_number} - {self.amount}"


# =========================
# RECHARGE LEVEL INCOME
# =========================

class RechargeLevelIncome(models.Model):

    recharge = models.ForeignKey(
        Recharge,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    from_user = models.ForeignKey(
        User,
        related_name='recharge_from_user',
        on_delete=models.CASCADE
    )

    level = models.IntegerField()

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - Level {self.level}"
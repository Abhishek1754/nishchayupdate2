from django.db import models
from decimal import Decimal
import uuid

from accounts.models import User


# =====================================================
# RECHARGE LEVEL SETTINGS
# =====================================================

class RechargeLevelSetting(models.Model):

    level = models.IntegerField()

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Recharge Level {self.level}"


# =====================================================
# RECHARGE PROVIDER
# =====================================================

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

    # REAL PROVIDER OPERATOR CODE

    operator_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    image = models.ImageField(
        upload_to='recharge/providers/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =====================================================
# RECHARGE TRANSACTION
# =====================================================

class Recharge(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),

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

    # UNIQUE INTERNAL TXN

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True
    )

    # PROVIDER TXN

    operator_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # PROVIDER REQUEST ID

    request_txn_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # API RESPONSE

    api_response = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # REFUND STATUS

    refund_processed = models.BooleanField(
        default=False
    )

    # FAILURE MESSAGE

    failure_message = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # AUTO GENERATE TXN ID

    def save(self, *args, **kwargs):

        if not self.transaction_id:

            self.transaction_id = (
                "RCHG" +
                str(uuid.uuid4()).replace('-', '')[:12].upper()
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.mobile_number} - {self.amount}"


# =====================================================
# RECHARGE LEVEL INCOME HISTORY
# =====================================================

class RechargeLevelIncome(models.Model):

    recharge = models.ForeignKey(
        Recharge,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recharge_income_user'
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


# =====================================================
# RECHARGE CASHBACK HISTORY
# =====================================================

class RechargeCashbackHistory(models.Model):

    recharge = models.ForeignKey(
        Recharge,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    cashback_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} Cashback"


# =====================================================
# WALLET TRANSACTION HISTORY
# =====================================================

class RechargeWalletHistory(models.Model):

    TRANSACTION_TYPES = (

        ('debit', 'Debit'),
        ('credit', 'Credit'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    recharge = models.ForeignKey(
        Recharge,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    message = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.transaction_type}"
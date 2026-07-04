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
        ('fastag', 'Fastag'),
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
# USER RECHARGE WALLET
# =====================================================

class RechargeWallet(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_added = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_spent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_cashback = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.user.email} Wallet"


# =====================================================
# ADD MONEY REQUEST
# =====================================================

class AddMoneyRequest(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),

    )

    PAYMENT_METHODS = (

        ('upi', 'UPI'),
        ('qr', 'QR'),
        ('bank', 'Bank Transfer'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    utr_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    screenshot = models.ImageField(
        upload_to='recharge/payment_screenshots/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    admin_note = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.amount}"


# =====================================================
# ADMIN PAYMENT SETTINGS
# =====================================================

class RechargePaymentGateway(models.Model):

    upi_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    qr_code = models.ImageField(
        upload_to='recharge/qr/',
        blank=True,
        null=True
    )

    account_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    bank_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    account_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    ifsc_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return "Recharge Payment Settings"


# =====================================================
# COUPON SYSTEM
# =====================================================

class RechargeCoupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    max_cashback = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    minimum_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    expiry_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.code


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
        on_delete=models.CASCADE,
        null=True,
        blank=True
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

    coupon = models.ForeignKey(
        RechargeCoupon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True
    )

    operator_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    request_txn_id = models.CharField(
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

    refund_processed = models.BooleanField(
        default=False
    )

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
# WALLET HISTORY
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

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    message = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.transaction_type}"
    
    
    
# =====================================================
# WITHDRAW REQUEST
# =====================================================

class RechargeWithdrawRequest(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),

    )

    METHOD_CHOICES = (

        ('upi', 'UPI'),
        ('bank', 'Bank'),
        ('paytm', 'Paytm'),
        ('gpay', 'Google Pay'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    withdraw_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES
    )

    account_name = models.CharField(
        max_length=255
    )

    account_details = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    admin_remark = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.user.email} - ₹{self.amount}"
    
    # =====================================================
# CASHFREE PAYMENT
# =====================================================

class RechargePayment(models.Model):

    STATUS_CHOICES = (

        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    order_id = models.CharField(
        max_length=150,
        unique=True
    )

    cf_payment_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    
    provider = models.ForeignKey(
    RechargeProvider,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    
    mobile_number = models.CharField(
    max_length=20,
    blank=True,
    null=True
)
    
    coupon = models.ForeignKey(
    RechargeCoupon,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    
    

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    wallet_credited = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.order_id


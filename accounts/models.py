from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):

    # =====================================================
    # BASIC DETAILS
    # =====================================================

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    # =====================================================
    # REFERRAL SYSTEM
    # =====================================================

    referral_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )

    referred_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='team_members'
    )

    # =====================================================
    # WALLET SYSTEM
    # =====================================================

    wallet_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    roi_wallet = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    recharge_wallet = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    ecommerce_wallet = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_earnings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_withdraw = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    nishchay_coin = models.IntegerField(
        default=0
    )

    # =====================================================
    # SUBSCRIPTION
    # =====================================================

    PLAN_CHOICES = (
        ('FREE', 'Free'),
        ('PREMIUM', 'Premium'),
    )

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default='FREE'
    )

    subscription_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    subscription_date = models.DateTimeField(
        null=True,
        blank=True
    )

    is_subscription_active = models.BooleanField(
        default=False
    )

    # =====================================================
    # ENTERPRISE ROLE SYSTEM
    # =====================================================

    is_admin = models.BooleanField(
        default=False
    )

    is_staff_user = models.BooleanField(
        default=False
    )

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
        ('shop', 'Shop'),
        ('delivery', 'Delivery'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    # =====================================================
    # ACCOUNT STATUS
    # =====================================================

    is_verified = models.BooleanField(
        default=False
    )

    is_blocked = models.BooleanField(
        default=False
    )
    
    # =====================================================
# PASSWORD RESET OTP
# =====================================================

    password_reset_otp = models.CharField(
    max_length=6,
    blank=True,
    null=True
    )

otp_created_at = models.DateTimeField(
    blank=True,
    null=True
)

    # =====================================================
    # TIMESTAMPS
    # =====================================================

created_at = models.DateTimeField(
        auto_now_add=True
    )

updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================================
    # SAVE METHOD
    # =====================================================

def save(self, *args, **kwargs):

        if not self.referral_code:
            self.referral_code = (
                str(uuid.uuid4())
                .replace('-', '')[:8]
                .upper()
            )

        if self.is_superuser:
            self.is_admin = True
            self.role = 'admin'

        super().save(*args, **kwargs)

    # =====================================================
    # TEAM COUNT
    # =====================================================

@property
def total_team(self):
        return self.team_members.count()

    # =====================================================
    # STRING METHOD
    # =====================================================

def __str__(self):
        return self.email
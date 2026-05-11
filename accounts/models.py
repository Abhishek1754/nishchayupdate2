from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    wallet_balance = models.FloatField(default=0)
    nishchay_coin = models.IntegerField(default=0)

    is_subscribed = models.BooleanField(default=False)

    # =========================
    # 🚀 ENTERPRISE ROLE SYSTEM
    # =========================
    is_admin = models.BooleanField(default=False)   # full access
    is_staff_user = models.BooleanField(default=False)  # limited access

    # Optional: role type (future ready)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # =========================
    # SAVE METHOD
    # =========================
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8]

        # 🔥 auto role assignment (enterprise logic)
        if self.is_superuser:
            self.is_admin = True
            self.role = 'admin'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
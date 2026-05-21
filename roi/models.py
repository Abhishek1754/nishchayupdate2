from django.db import models
from django.utils import timezone
from datetime import timedelta

# 🚀 AI KARMA IMPORT
from ai_karma.fraud_engine import detect_roi_fraud


# =========================
# ROI PLAN
# =========================

class ROIPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # DAILY ROI %
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    # MATURITY DAYS
    maturity_days = models.IntegerField(
        default=30
    )

    # MATURITY AMOUNT
    maturity_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # LEVEL INCOME %
    level_income_percentage = models.DecimalField(
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
# USER INVESTMENT
# =========================

class Investment(models.Model):

    STATUS_CHOICES = (

        ('active', 'Active'),

        ('completed', 'Completed'),

    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    plan = models.ForeignKey(
        ROIPlan,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # DAILY INCOME
    daily_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # TOTAL EARNED
    total_earned = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # START DATE
    start_date = models.DateTimeField(
        auto_now_add=True
    )

    # END DATE
    end_date = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # CREATED TIME
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.amount}"

    # =========================
    # SAVE METHOD
    # =========================

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        # DAILY ROI CALCULATION

        if self.plan:

            self.daily_income = (

                self.amount *

                self.plan.percentage

            ) / 100

            # MATURITY DATE

            self.end_date = (

                timezone.now() +

                timedelta(
                    days=self.plan.maturity_days
                )

            )

        super().save(*args, **kwargs)

        # =========================
        # AI KARMA FRAUD CHECK
        # =========================

        if is_new:

            detect_roi_fraud(
                self.user,
                self.amount
            )

            # =========================
            # LEVEL INCOME
            # =========================

            sponsor = self.user.referred_by

            if sponsor:

                level_income = (

                    self.amount *

                    self.plan.level_income_percentage

                ) / 100

                sponsor.wallet_balance += level_income

                sponsor.save()


# =========================
# DAILY ROI INCOME
# =========================

class DailyROIIncome(models.Model):

    investment = models.ForeignKey(
        Investment,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.amount}"


# =========================
# WITHDRAW REQUEST
# =========================

class WithdrawRequest(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),

        ('approved', 'Approved'),

        ('rejected', 'Rejected'),

    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    wallet_type = models.CharField(
        max_length=50,
        default='main_wallet'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # USER CAN WITHDRAW AFTER 7 DAYS
    withdraw_available_date = models.DateTimeField(
        default=timezone.now
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if not self.pk:

            self.withdraw_available_date = (

                timezone.now() +

                timedelta(days=7)

            )

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.user.email} - {self.amount}"
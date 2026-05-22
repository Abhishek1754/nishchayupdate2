from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# AI KARMA IMPORT
from ai_karma.fraud_engine import detect_roi_fraud


# =========================
# ROI LEVEL SETTINGS
# =========================

class ROILevelIncome(models.Model):

    level = models.IntegerField()

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"ROI Level {self.level} - {self.percentage}%"


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

            ) / Decimal(100)

            # MATURITY DATE

            self.end_date = (

                timezone.now() +

                timedelta(
                    days=self.plan.maturity_days
                )

            )

        super().save(*args, **kwargs)

        # =========================
        # AFTER NEW INVESTMENT
        # =========================

        if is_new:

            # =========================
            # AI FRAUD CHECK
            # =========================

            detect_roi_fraud(
                self.user,
                self.amount
            )

            # =========================
            # DISTRIBUTE LEVEL INCOME
            # =========================

            self.distribute_level_income()

    # =========================
    # LEVEL INCOME FUNCTION
    # =========================

    def distribute_level_income(self):

        sponsor = self.user.referred_by

        current_level = 1

        while sponsor and current_level <= 6:

            try:

                level_setting = ROILevelIncome.objects.get(
                    level=current_level
                )

                level_percentage = level_setting.percentage

            except ROILevelIncome.DoesNotExist:

                level_percentage = Decimal(0)

            # LEVEL INCOME

            level_income = (

                self.amount *

                level_percentage

            ) / Decimal(100)

            # CREDIT WALLET

            sponsor.wallet_balance += level_income

            sponsor.save()

            # SAVE HISTORY

            ROILevelIncomeHistory.objects.create(

                user=sponsor,

                from_user=self.user,

                investment=self,

                level=current_level,

                percentage=level_percentage,

                amount=level_income

            )

            # NEXT LEVEL

            sponsor = sponsor.referred_by

            current_level += 1


# =========================
# ROI LEVEL INCOME HISTORY
# =========================

class ROILevelIncomeHistory(models.Model):

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='roi_income_receiver'
    )

    from_user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='roi_income_from_user'
    )

    investment = models.ForeignKey(
        Investment,
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
    
    # =========================
# ROI MONTHLY SALARY PLAN
# =========================

class ROIMonthlySalaryPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    minimum_direct_team = models.IntegerField(
        default=20
    )

    minimum_total_team = models.IntegerField(
        default=100
    )

    minimum_business = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    maximum_business = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
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
# ROI MONTHLY SALARY INCOME
# =========================

class ROIMonthlySalaryIncome(models.Model):

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    salary_plan = models.ForeignKey(
        ROIMonthlySalaryPlan,
        on_delete=models.CASCADE
    )

    total_business = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    direct_team = models.IntegerField(
        default=0
    )

    total_team = models.IntegerField(
        default=0
    )

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    salary_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    month = models.IntegerField()

    year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.month}/{self.year}"


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
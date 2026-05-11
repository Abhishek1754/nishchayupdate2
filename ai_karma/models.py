from django.db import models
from accounts.models import User


# =========================
# FRAUD ALERT MODEL
# =========================
class FraudAlert(models.Model):

    RISK_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    ALERT_TYPES = (
        ('roi', 'ROI Fraud'),
        ('wallet', 'Wallet Abuse'),
        ('referral', 'Referral Abuse'),
        ('login', 'Login Anomaly'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVELS,
        default='low'
    )

    reason = models.TextField()

    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.alert_type}"


# =========================
# AI RISK SCORE ENGINE
# =========================
class RiskScore(models.Model):

    LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    score = models.IntegerField(default=0)

    risk_level = models.CharField(
        max_length=20,
        choices=LEVELS,
        default='low'
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.score}"
from django.db import models

# 🚀 AI KARMA IMPORT
from ai_karma.fraud_engine import detect_roi_fraud


class ROIPlan(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    percentage = models.FloatField()

    def __str__(self):
        return self.name


class Investment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    plan = models.ForeignKey(ROIPlan, on_delete=models.CASCADE)
    amount = models.FloatField()

    # ✅ CREATED TIME
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"

    # 🚀 AI KARMA FRAUD CHECK
    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        # 🔥 only on new investment
        if is_new:
            detect_roi_fraud(self.user, self.amount)
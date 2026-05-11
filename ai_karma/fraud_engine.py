from .models import FraudAlert, RiskScore

# 🚀 WEBSOCKET IMPORTS
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# =========================
# UPDATE AI RISK SCORE
# =========================
def update_risk_score(user, points):

    risk, created = RiskScore.objects.get_or_create(
        user=user
    )

    # 🔥 Increase score
    risk.score += points

    # 🚨 LEVEL LOGIC
    if risk.score >= 80:
        risk.risk_level = 'critical'

    elif risk.score >= 50:
        risk.risk_level = 'high'

    elif risk.score >= 20:
        risk.risk_level = 'medium'

    else:
        risk.risk_level = 'low'

    risk.save()

    return risk


# =========================
# CREATE FRAUD ALERT
# =========================
def create_alert(user, alert_type, risk_level, reason):

    # 🚨 Avoid duplicate unresolved alerts
    existing = FraudAlert.objects.filter(
        user=user,
        alert_type=alert_type,
        reason=reason,
        is_resolved=False
    ).first()

    if existing:
        return existing

    # 🚨 CREATE ALERT
    alert = FraudAlert.objects.create(
        user=user,
        alert_type=alert_type,
        risk_level=risk_level,
        reason=reason
    )

    # =========================
    # 🔥 REALTIME WEBSOCKET ALERT
    # =========================
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "ai_karma_alerts",
        {
            "type": "send_alert",
            "message": reason,
            "risk_level": risk_level,
        }
    )

    return alert


# =========================
# ROI FRAUD DETECTION
# =========================
def detect_roi_fraud(user, amount):

    # 🚨 VERY HIGH ROI INVESTMENT
    if amount >= 50000:

        create_alert(
            user=user,
            alert_type='roi',
            risk_level='high',
            reason=f"Suspicious ROI investment detected: ₹{amount}"
        )

        # 🔥 Increase AI score
        update_risk_score(user, 25)

        return True

    return False
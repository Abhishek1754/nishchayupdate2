from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate

from .models import User
from roi.models import Investment
from roi.models import Investment, ROIPlan
from ecommerce.models import Product
from ecommerce.models import Product, Order
from django.http import JsonResponse
from ai_karma.models import RiskScore

# =========================
# REGISTER API
# =========================
@api_view(['POST'])
def register(request):
    data = request.data

    ref_user = None
    if data.get('referral_code'):
        ref_user = User.objects.filter(referral_code=data['referral_code']).first()

    user = User.objects.create(
        username=data['email'],
        email=data['email'],
        phone=data['phone'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        state=data['state'],
        pincode=data['pincode'],
        password=make_password(data['password']),
        referred_by=ref_user
    )

    # Signup bonus
    user.nishchay_coin += 1
    user.wallet_balance += 1
    user.save()

    if ref_user:
        ref_user.nishchay_coin += 1
        ref_user.wallet_balance += 1
        ref_user.save()

    return Response({"msg": "Registered"})


# =========================
# LOGIN API
# =========================
@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data['email'],
        password=request.data['password']
    )

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    token = RefreshToken.for_user(user)

    return Response({
        "access": str(token.access_token),
        "refresh": str(token)
    })


# =========================
# DASHBOARD VIEW (MAIN)
# =========================
# =========================
# DASHBOARD VIEW (MAIN)
# =========================
def dashboard_view(request):

    # =========================
    # BASIC STATS
    # =========================
    total_users = User.objects.count()

    total_revenue = Investment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_roi = Investment.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    # =========================
    # CHART DATA (LAST 7 DAYS)
    # =========================
    last_7_days = timezone.now() - timedelta(days=7)

    data = (
        Investment.objects
        .filter(created_at__gte=last_7_days)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    labels = []
    chart_data = []

    for item in data:
        labels.append(item['date'].strftime('%d %b'))
        chart_data.append(item['total'] or 0)

    # ⚠️ fallback if no data
    if not labels:
        labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        chart_data = [100, 200, 150, 300, 250]

    # =========================
    # MODULE SUMMARY
    # =========================
    module_labels = ["Ecommerce", "ROI", "Recharge", "Astrology", "Career"]
    module_values = [
        total_products,
        ROIPlan.objects.count(),
        10,  # replace later
        5,
        3
    ]

    # =========================
    # LATEST ORDERS (NEW)
    # =========================
    latest_orders = Order.objects.select_related('user').order_by('-id')[:5]

    # =========================
    # CONTEXT
    # =========================
    context = {
        'total_users': total_users,
        'total_revenue': total_revenue,
        'total_roi': total_roi,
        'total_products': total_products,
        'total_orders': total_orders,

        'chart_labels': labels,
        'chart_data': chart_data,

        'module_labels': module_labels,
        'module_values': module_values,

        'latest_orders': latest_orders,
    }

    return render(request, 'dashboard.html', context)





def dashboard_api(request):
    total_users = User.objects.count()
    total_revenue = Investment.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_roi = Investment.objects.count()
    total_orders = Order.objects.count()

    # latest orders
    latest_orders = list(
        Order.objects.select_related('user')
        .order_by('-id')[:5]
        .values('id', 'user__email', 'status')
    )

    # 🔥 CHART DATA (LAST 7 DAYS)
    last_7_days = timezone.now() - timedelta(days=7)

    data = (
        Investment.objects
        .filter(created_at__gte=last_7_days)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    labels = [str(i['date']) for i in data]
    chart_data = [i['total'] or 0 for i in data]

    if not labels:
        labels = ["Mon","Tue","Wed","Thu","Fri"]
        chart_data = [100,200,150,300,250]

    return JsonResponse({
        "total_users": total_users,
        "total_revenue": total_revenue,
        "total_roi": total_roi,
        "total_orders": total_orders,
        "latest_orders": latest_orders,
        "chart_labels": labels,
        "chart_data": chart_data,
    })
    
    
# =========================
# AI KARMA DASHBOARD
# =========================

# =========================
# AI KARMA DASHBOARD
# =========================

from ai_karma.models import FraudAlert


def ai_karma_dashboard(request):

    # 🚨 TOTAL ALERTS
    total_alerts = FraudAlert.objects.count()

    # 🚨 HIGH RISK ALERTS
    high_risk = FraudAlert.objects.filter(
        risk_level='high'
    ).count()

    # 🚨 CRITICAL ALERTS
    critical_risk = FraudAlert.objects.filter(
        risk_level='critical'
    ).count()

    # 🚨 LATEST ALERTS
    latest_alerts = FraudAlert.objects.select_related(
        'user'
    ).order_by('-created_at')[:5]

    context = {
        'total_alerts': total_alerts,
        'high_risk': high_risk,
        'critical_risk': critical_risk,
        'latest_alerts': latest_alerts,
    }

    return render(request, 'ai_karma_dashboard.html', context)
    
  
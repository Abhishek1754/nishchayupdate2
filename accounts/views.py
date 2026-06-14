
from recharge.models import RechargeWallet
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate

from .models import User

from roi.models import Investment, ROIPlan

from ecommerce.models import Product, Order

from ai_karma.models import RiskScore, FraudAlert

import random

from django.core.mail import send_mail

from django.conf import settings

from django.utils import timezone


# =========================
# REGISTER API
# =========================

# =========================
# REGISTER API
# =========================

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    data = request.data

    # =========================
    # VALIDATIONS
    # =========================

    if User.objects.filter(email=data['email']).exists():

        return Response({

            "error": "Email already exists"

        }, status=400)

    if User.objects.filter(phone=data['phone']).exists():

        return Response({

            "error": "Phone already exists"

        }, status=400)

    # =========================
    # REFERRAL USER
    # =========================

    ref_user = None

    if data.get('referral_code'):

        ref_user = User.objects.filter(
            referral_code=data['referral_code']
        ).first()

    # =========================
    # CREATE USER
    # =========================

    user = User.objects.create(

    username=data['email'],

    email=data['email'],

    phone=data['phone'],

    first_name=data['first_name'],

    last_name=data['last_name'],

        state=data['state'],

        pincode=data['pincode'],

        password=make_password(
            data['password']
        ),

        referred_by=ref_user

    )

    # =========================
    # FREE BONUS
    # =========================

    user.wallet_balance += 1

    user.nishchay_coin += 2

    user.save()

    # =========================
    # REFERRAL BONUS
    # =========================

    if ref_user:

        ref_user.wallet_balance += 1

        ref_user.nishchay_coin += 1

        ref_user.save()

    # =========================
    # RESPONSE
    # =========================

    return Response({

        "msg": "Registration Successful",

        "wallet_balance": user.wallet_balance,

        "nishchay_coin": user.nishchay_coin,

        "referral_code": user.referral_code,

    }, status=201)
# =========================
# LOGIN API
# =========================

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = authenticate(

        username=request.data['email'],

        password=request.data['password']

    )

    if not user:

        return Response({

            "error": "Invalid credentials"

        }, status=400)

    token = RefreshToken.for_user(user)

    return Response({

    "access": str(token.access_token),

    "refresh": str(token),

    "username": user.first_name,

    "email": user.email,

    "wallet_balance": user.wallet_balance,

    "nishchay_coin": user.nishchay_coin,

    "referral_code": user.referral_code,

})


# =========================
# USER PROFILE API
# =========================

@api_view(['GET'])
def profile(request):

    wallet, created = RechargeWallet.objects.get_or_create(
        user=request.user
    )

    return Response({

        "email": request.user.email,

        "phone": request.user.phone,

        "wallet_balance": str(wallet.balance),

        "total_added": str(wallet.total_added),

        "total_spent": str(wallet.total_spent),

        "total_cashback": str(wallet.total_cashback),

        "nishchay_coin": request.user.nishchay_coin,

        "referral_code": request.user.referral_code,

        "subscription": request.user.is_subscribed,

    })

# =========================
# DASHBOARD VIEW
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
    # CHART DATA
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

        labels.append(
            item['date'].strftime('%d %b')
        )

        chart_data.append(
            item['total'] or 0
        )

    # FALLBACK DATA

    if not labels:

        labels = [

            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri"

        ]

        chart_data = [

            100,
            200,
            150,
            300,
            250

        ]

    # =========================
    # MODULE SUMMARY
    # =========================

    module_labels = [

        "Ecommerce",
        "ROI",
        "Recharge",
        "Astrology",
        "Career"

    ]

    module_values = [

        total_products,

        ROIPlan.objects.count(),

        10,

        5,

        3

    ]

    # =========================
    # LATEST ORDERS
    # =========================

    latest_orders = (

        Order.objects

        .select_related('user')

        .order_by('-id')[:5]

    )

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

    return render(
        request,
        'dashboard.html',
        context
    )


# =========================
# DASHBOARD API
# =========================

def dashboard_api(request):

    total_users = User.objects.count()

    total_revenue = Investment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_roi = Investment.objects.count()

    total_orders = Order.objects.count()

    latest_orders = list(

        Order.objects

        .select_related('user')

        .order_by('-id')[:5]

        .values(

            'id',

            'user__email',

            'status'

        )

    )

    last_7_days = timezone.now() - timedelta(days=7)

    data = (

        Investment.objects

        .filter(created_at__gte=last_7_days)

        .annotate(date=TruncDate('created_at'))

        .values('date')

        .annotate(total=Sum('amount'))

        .order_by('date')

    )

    labels = [

        str(i['date'])

        for i in data

    ]

    chart_data = [

        i['total'] or 0

        for i in data

    ]

    if not labels:

        labels = [

            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri"

        ]

        chart_data = [

            100,
            200,
            150,
            300,
            250

        ]

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

def ai_karma_dashboard(request):

    total_alerts = FraudAlert.objects.count()

    high_risk = FraudAlert.objects.filter(
        risk_level='high'
    ).count()

    critical_risk = FraudAlert.objects.filter(
        risk_level='critical'
    ).count()

    latest_alerts = (

        FraudAlert.objects

        .select_related('user')

        .order_by('-created_at')[:5]

    )

    context = {

        'total_alerts': total_alerts,

        'high_risk': high_risk,

        'critical_risk': critical_risk,

        'latest_alerts': latest_alerts,

    }

    return render(
        request,
        'ai_karma_dashboard.html',
        context
    )


# =========================
# HOME PAGE
# =========================

# =========================
# HOME PAGE
# =========================

def home(request):

    return render(
        request,
        'home/index.html'
    )


# =========================
# FRONTEND LOGIN PAGE
# =========================

def user_login_page(request):

    return render(
        request,
        'accounts/login.html'
    )


# =========================
# FRONTEND REGISTER PAGE
# =========================

def user_register_page(request):

    return render(
        request,
        'accounts/register.html'
    )
    
# =========================
# FORGOT PASSWORD PAGE
# =========================

def forgot_password_page(request):

    return render(
        request,
        'accounts/forgot_password.html'
    )


# =========================
# VERIFY OTP PAGE
# =========================

def verify_otp_page(request):

    return render(
        request,
        'accounts/verify_otp.html'
    )


# =========================
# RESET PASSWORD PAGE
# =========================

def reset_password_page(request):

    return render(
        request,
        'accounts/reset_password.html'
    )
    
    
# =========================
# SEND RESET OTP
# =========================

@api_view(['POST'])
@permission_classes([AllowAny])
def send_reset_otp(request):

    email = request.data.get(
        'email'
    )

    try:

        user = User.objects.get(
            email=email
        )

    except User.DoesNotExist:

        return Response(

            {

                "error":

                "Email not found"

            },

            status=400

        )

    # Generate 6-digit OTP

    otp = str(

        random.randint(

            100000,

            999999

        )

    )

    # Save OTP

    user.password_reset_otp = otp

    user.otp_created_at = timezone.now()

    user.save()

    # Send Email

    send_mail(

        subject='Nishchay Password Reset OTP',

        message=

        f'''

Hello {user.first_name},

Your password reset OTP is:

{otp}

This OTP is valid for 10 minutes.

Regards,

Nishchay Multiverse

https://nishchay.in

''',

        from_email=settings.EMAIL_HOST_USER,

        recipient_list=[email],

        fail_silently=False

    )

    return Response(

        {

            "message":

            "OTP sent successfully"

        }

    )
    
    
    # =========================
# VERIFY RESET OTP
# =========================

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_otp(request):

    email = request.data.get(
        'email'
    )

    otp = request.data.get(
        'otp'
    )

    try:

        user = User.objects.get(
            email=email
        )

    except User.DoesNotExist:

        return Response(

            {

                "error":

                "User not found"

            },

            status=400

        )

    if user.password_reset_otp != otp:

        return Response(

            {

                "error":

                "Invalid OTP"

            },

            status=400

        )

    # Check expiry

    if timezone.now() > (

        user.otp_created_at +

        timedelta(minutes=10)

    ):

        return Response(

            {

                "error":

                "OTP expired"

            },

            status=400

        )

    return Response(

        {

            "message":

            "OTP verified successfully"

        }

    )
    
    # =========================
# RESET PASSWORD
# =========================

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):

    email = request.data.get(
        'email'
    )

    new_password = request.data.get(
        'new_password'
    )

    confirm_password = request.data.get(
        'confirm_password'
    )

    try:

        user = User.objects.get(
            email=email
        )

    except User.DoesNotExist:

        return Response(

            {

                "error":

                "User not found"

            },

            status=400

        )

    if new_password != confirm_password:

        return Response(

            {

                "error":

                "Passwords do not match"

            },

            status=400

        )

    # Set new password

    user.set_password(
        new_password
    )

    # Clear OTP

    user.password_reset_otp = None

    user.otp_created_at = None

    user.save()

    return Response(

        {

            "message":

            "Password changed successfully"

        }

    )
    

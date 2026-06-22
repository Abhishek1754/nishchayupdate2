
from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import SubscriptionPlan, UserSubscription

import uuid
import requests


# =====================================================
# GET PLAN API
# =====================================================

@api_view(['GET'])
def get_plan(request):

    plan = SubscriptionPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return Response({
            "message": "No plan found"
        })

    return Response({

        "name": plan.name,
        "price": plan.price,
        "reward_amount": plan.reward_amount,
        "reward_coin": plan.reward_coin,
        "validity_days": plan.validity_days

    })


# =====================================================
# ACTIVATE SUBSCRIPTION API
# =====================================================

@api_view(['POST'])
def activate_subscription(request):

    user = request.user

    plan = SubscriptionPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return Response({
            "message": "No active plan"
        })

    expiry_date = timezone.now() + timedelta(
        days=plan.validity_days
    )

    user.plan = "PREMIUM"
    user.is_subscription_active = True
    user.subscription_amount = plan.price
    user.subscription_date = timezone.now()

    user.wallet_balance += 2
    user.nishchay_coin += 10

    user.save()

    UserSubscription.objects.create(

        user=user,
        plan=plan,
        amount=plan.price,
        expiry_date=expiry_date

    )

    return Response({

        "message": "Subscription activated successfully"

    })


# =====================================================
# PAYMENT PAGE
# =====================================================

def subscription_payment_page(request):

    plan = SubscriptionPlan.objects.filter(
        is_active=True
    ).first()

    return render(

        request,
        "subscription/payment.html",
        {
            "plan": plan
        }

    )


# =====================================================
# PAYMENT SUCCESS PAGE
# =====================================================

def payment_success_page(request):

    if request.user.is_authenticated:

        plan = SubscriptionPlan.objects.filter(
            is_active=True
        ).first()

        expiry_date = timezone.now() + timedelta(
            days=plan.validity_days
        )

        user = request.user

        user.plan = "PREMIUM"
        user.is_subscription_active = True
        user.subscription_amount = plan.price
        user.subscription_date = timezone.now()

        user.wallet_balance += 2
        user.nishchay_coin += 10

        user.save()

        already_exists = UserSubscription.objects.filter(
            user=user,
            status="ACTIVE"
        ).exists()

        if not already_exists:

            UserSubscription.objects.create(

                user=user,
                plan=plan,
                amount=plan.price,
                expiry_date=expiry_date

            )

    return render(
        request,
        "subscription/payment_success.html"
    )


# =====================================================
# CREATE CASHFREE ORDER
# =====================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def create_cashfree_order(request):

    plan = SubscriptionPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return Response({
            "message": "No active plan"
        })

    order_id = str(uuid.uuid4())

    payload = {

        "order_id": order_id,

        "order_amount": float(plan.price),

        "order_currency": "INR",

        "customer_details": {

            "customer_id": order_id,

            "customer_email": "nishchaymultiverse@gmail.com",

            "customer_phone": "9876543210"

        },

        "order_meta": {

            "return_url":
            "https://nishchay.in/api/subscription/success/?order_id={order_id}"

        }

    }

    headers = {

        "x-client-id":
        settings.CASHFREE_APP_ID,

        "x-client-secret":
        settings.CASHFREE_SECRET_KEY,

        "x-api-version":
        "2023-08-01",

        "Content-Type":
        "application/json"

    }

    response = requests.post(

        "https://api.cashfree.com/pg/orders",

        json=payload,

        headers=headers

    )

    return JsonResponse(
        response.json(),
        safe=False
    )

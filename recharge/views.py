from django.shortcuts import render
from decimal import Decimal
import requests
import uuid
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .models import (
    RechargeProvider,
    Recharge,
    RechargeLevelIncome,
    RechargeLevelSetting,
    RechargeCashbackHistory,
)

from accounts.models import User


# =====================================================
# API TOKEN
# =====================================================

API_TOKEN = "b12418e1-7d26-4c68-b968-d2a0a368f082"


# =====================================================
# UI PAGES
# =====================================================

def recharge_home(request):
    return render(request, 'recharge/index.html')


def mobile_recharge(request):
    return render(request, 'recharge/mobile.html')


def recharge_payment(request):
    return render(request, 'recharge/payment/index.html')


def recharge_success(request):
    return render(request, 'recharge/success/index.html')


def transaction_history(request):
    return render(request, 'recharge/transactions/index.html')


def refer_earn(request):
    return render(request, 'recharge/refer/index.html')


def profile_page(request):
    return render(request, 'recharge/profile/index.html')


def withdraw_page(request):
    return render(request, 'recharge/withdraw/index.html')


def offers_page(request):
    return render(request, 'recharge/offers/index.html')


def notifications_page(request):
    return render(request, 'recharge/notifications/index.html')


def support_page(request):
    return render(request, 'recharge/support/index.html')


# =====================================================
# ALL PROVIDERS API
# =====================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def recharge_providers(request):

    providers = RechargeProvider.objects.filter(
        is_active=True
    )

    data = []

    for provider in providers:

        data.append({

            "id": provider.id,
            "name": provider.name,
            "operator_code": provider.operator_code,
            "service_type": provider.service_type,
            "cashback_percentage": str(
                provider.cashback_percentage
            )

        })

    return Response(data)


# =====================================================
# DO RECHARGE
# =====================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def do_recharge(request):

    try:

        mobile_number = request.data.get(
            'mobile_number'
        )

        amount = request.data.get(
            'amount'
        )

        provider_id = request.data.get(
            'provider_id'
        )

        # =====================================================
        # VALIDATION
        # =====================================================

        if not provider_id:

            return Response({

                "status": False,
                "message": "Provider required"

            }, status=400)

        if not mobile_number:

            return Response({

                "status": False,
                "message": "Mobile number required"

            }, status=400)

        if not amount:

            return Response({

                "status": False,
                "message": "Amount required"

            }, status=400)

        provider = RechargeProvider.objects.get(
            id=provider_id
        )

        # =====================================================
        # CREATE TRANSACTION ID
        # =====================================================

        transaction_id = str(
            uuid.uuid4()
        ).replace('-', '')[:15]

        # =====================================================
        # API URL
        # =====================================================

        recharge_url = (

            f"https://ultra.myfinpaypro.co.in/api/Service/Recharge2?"
            f"ApiToken={API_TOKEN}"
            f"&MobileNo={mobile_number}"
            f"&Amount={amount}"
            f"&OpId={provider.operator_code}"
            f"&RefTxnId={transaction_id}"

        )

        print(recharge_url)

        # =====================================================
        # API CALL
        # =====================================================

        response = requests.get(
            recharge_url,
            timeout=30
        )

        api_data = response.json()

        print(api_data)

        # =====================================================
        # STATUS
        # =====================================================

        api_status = str(
            api_data.get('STATUS')
        )

        api_message = api_data.get(
            'MESSAGE',
            'Recharge Failed'
        )

        # =====================================================
        # SUCCESS
        # =====================================================

        if api_status == "1":

            recharge = Recharge.objects.create(

                user=None,

                provider=provider,

                mobile_number=mobile_number,

                amount=Decimal(amount),

                cashback=0,

                status='success',

                transaction_id=transaction_id,

                operator_reference=api_data.get(
                    "OPTXNID"
                ),

                api_response=json.dumps(api_data)

            )

            return Response({

                "status": True,

                "message": api_message,

                "transaction_id": transaction_id,

                "api_response": api_data

            })

        # =====================================================
        # FAILED
        # =====================================================

        Recharge.objects.create(

            user=None,

            provider=provider,

            mobile_number=mobile_number,

            amount=Decimal(amount),

            cashback=0,

            status='failed',

            transaction_id=transaction_id,

            api_response=json.dumps(api_data)

        )

        return Response({

            "status": False,

            "message": api_message,

            "api_response": api_data

        }, status=400)

    except Exception as e:

        print(str(e))

        return Response({

            "status": False,

            "message": str(e)

        }, status=500)


# =====================================================
# MY RECHARGES
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_recharges(request):

    recharges = Recharge.objects.filter(
        user=request.user
    ).order_by('-id')

    data = []

    for recharge in recharges:

        data.append({

            "id": recharge.id,
            "provider": recharge.provider.name,
            "mobile_number": recharge.mobile_number,
            "amount": str(recharge.amount),
            "cashback": str(recharge.cashback),
            "status": recharge.status,
            "transaction_id": recharge.transaction_id,
            "operator_reference": recharge.operator_reference,
            "created_at": recharge.created_at,

        })

    return Response(data)
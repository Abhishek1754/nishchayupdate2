from django.shortcuts import render
from decimal import Decimal
import requests
import uuid
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


from wallet.utils import create_wallet_transaction

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

        provider = RechargeProvider.objects.get(
            id=provider_id
        )

        recharge = Recharge.objects.create(

            user=None,

            provider=provider,

            mobile_number=mobile_number,

            amount=amount,

            cashback=0,

            status='pending'

        )

        recharge.status = 'success'

        recharge.transaction_id = f"TXN{recharge.id}"

        recharge.save()

        return Response({

            "status": True,
            "message": "Recharge Successful",
            "transaction_id": recharge.transaction_id

        })

    except Exception as e:

        return Response({

            "status": False,
            "message": str(e)

        })
    # =====================================================
    # VALIDATION
    # =====================================================

    if not provider_id:

        return Response({

            "status": "failed",
            "message": "Provider required"

        }, status=400)

    if not mobile_number:

        return Response({

            "status": "failed",
            "message": "Mobile number required"

        }, status=400)

    if not amount:

        return Response({

            "status": "failed",
            "message": "Amount required"

        }, status=400)

    amount = Decimal(str(amount))

    try:

        provider = RechargeProvider.objects.get(
            id=provider_id,
            is_active=True
        )

    except RechargeProvider.DoesNotExist:

        return Response({

            "status": "failed",
            "message": "Provider not found"

        }, status=404)

    # =====================================================
    # CHECK WALLET
    # =====================================================

    if user.wallet_balance < amount:

        return Response({

            "status": "failed",
            "message": "Insufficient wallet balance"

        }, status=400)

    # =====================================================
    # UNIQUE TRANSACTION ID
    # =====================================================

    request_txn_id = str(
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
        f"&RefTxnId={request_txn_id}"

    )

    try:

        response = requests.get(
            recharge_url,
            timeout=30
        )

        api_data = response.json()

    except Exception as e:

        return Response({

            "status": "failed",
            "message": "Recharge server error",
            "error": str(e)

        }, status=500)

    # =====================================================
    # API RESPONSE
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

        # DEDUCT USER WALLET

        user.wallet_balance -= amount

        # CASHBACK

        cashback = (

            amount *

            Decimal(
                provider.cashback_percentage
            )

        ) / Decimal(100)

        user.wallet_balance += cashback

        user.save()

        # =====================================================
        # WALLET HISTORY
        # =====================================================

        create_wallet_transaction(

            user=user,

            transaction_type='debit',

            source='recharge',

            amount=amount,

            remark='Recharge Successful'

        )

        if cashback > 0:

            create_wallet_transaction(

                user=user,

                transaction_type='credit',

                source='recharge',

                amount=cashback,

                remark='Recharge Cashback'

            )

        # =====================================================
        # SAVE RECHARGE
        # =====================================================

        recharge = Recharge.objects.create(

            user=user,

            provider=provider,

            mobile_number=mobile_number,

            amount=amount,

            cashback=cashback,

            status='success',

            transaction_id=request_txn_id,

            operator_reference=api_data.get(
                "OPTXNID"
            ),

            api_response=json.dumps(api_data)

        )

        # =====================================================
        # CASHBACK HISTORY
        # =====================================================

        RechargeCashbackHistory.objects.create(

            recharge=recharge,

            user=user,

            cashback_percentage=provider.cashback_percentage,

            cashback_amount=cashback

        )

        # =====================================================
        # LEVEL INCOME
        # =====================================================

        current_user = user.referred_by

        current_level = 1

        while current_user and current_level <= 3:

            try:

                level_setting = RechargeLevelSetting.objects.get(
                    level=current_level
                )

                percentage = level_setting.percentage

            except RechargeLevelSetting.DoesNotExist:

                percentage = Decimal(0)

            income = (

                amount *

                percentage

            ) / Decimal(100)

            if income > 0:

                current_user.wallet_balance += income

                current_user.save()

                create_wallet_transaction(

                    user=current_user,

                    transaction_type='credit',

                    source='recharge',

                    amount=income,

                    remark=f'Level {current_level} Recharge Income'

                )

                RechargeLevelIncome.objects.create(

                    recharge=recharge,

                    user=current_user,

                    from_user=user,

                    level=current_level,

                    percentage=percentage,

                    amount=income

                )

            current_user = current_user.referred_by

            current_level += 1

        return Response({

            "status": "success",

            "message": api_message,

            "recharge_id": recharge.id,

            "cashback": str(cashback),

            "wallet_balance": str(
                user.wallet_balance
            ),

            "api_response": api_data

        })

    # =====================================================
    # FAILED
    # =====================================================

    Recharge.objects.create(

        user=user,

        provider=provider,

        mobile_number=mobile_number,

        amount=amount,

        cashback=0,

        status='failed',

        transaction_id=request_txn_id,

        api_response=json.dumps(api_data)

    )

    return Response({

        "status": "failed",

        "message": api_message,

        "api_response": api_data

    }, status=400)


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
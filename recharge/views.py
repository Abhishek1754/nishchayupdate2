from django.shortcuts import render
from decimal import Decimal
import requests
import uuid
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

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

    return render(
        request,
        'recharge/index.html'
    )


def mobile_recharge(request):

    return render(
        request,
        'recharge/mobile.html'
    )


def recharge_payment(request):

    return render(
        request,
        'recharge/payment/index.html'
    )


def recharge_success(request):

    return render(
        request,
        'recharge/success/index.html'
    )


def transaction_history(request):

    return render(
        request,
        'recharge/transactions/index.html'
    )


def refer_earn(request):

    return render(
        request,
        'recharge/refer/index.html'
    )


def profile_page(request):

    return render(
        request,
        'recharge/profile/index.html'
    )


def withdraw_page(request):

    return render(
        request,
        'recharge/withdraw/index.html'
    )


def offers_page(request):

    return render(
        request,
        'recharge/offers/index.html'
    )


def notifications_page(request):

    return render(
        request,
        'recharge/notifications/index.html'
    )


def support_page(request):

    return render(
        request,
        'recharge/support/index.html'
    )


# =====================================================
# ALL PROVIDERS
# =====================================================

@api_view(['GET'])
def recharge_providers(request):

    providers = RechargeProvider.objects.filter(
        is_active=True
    )

    data = []

    for provider in providers:

        data.append({

            "id": provider.id,
            "name": provider.name,
            "service_type": provider.service_type,
            "operator_code": provider.operator_code,
            "cashback_percentage": str(
                provider.cashback_percentage
            )

        })

    return Response(data)


# =====================================================
# RECHARGE API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def do_recharge(request):

    user = request.user

    provider_id = request.data.get(
        'provider_id'
    )

    mobile_number = request.data.get(
        'mobile_number'
    )

    amount = request.data.get(
        'amount'
    )

    if not provider_id:

        return Response({

            "error": "provider_id required"

        }, status=400)

    if not mobile_number:

        return Response({

            "error": "mobile number required"

        }, status=400)

    if not amount:

        return Response({

            "error": "amount required"

        }, status=400)

    amount = Decimal(amount)

    try:

        provider = RechargeProvider.objects.get(
            id=provider_id,
            is_active=True
        )

    except RechargeProvider.DoesNotExist:

        return Response({

            "error": "Provider not found"

        }, status=404)

    # =====================================================
    # CHECK WALLET
    # =====================================================

    if user.wallet_balance < amount:

        return Response({

            "error": "Insufficient Wallet Balance"

        }, status=400)

    # =====================================================
    # CREATE UNIQUE TXN ID
    # =====================================================

    request_txn_id = str(uuid.uuid4()).replace(
        '-',
        ''
    )[:15]

    # =====================================================
    # RECHARGE API URL
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

        api_request = requests.get(
            recharge_url,
            timeout=30
        )

        api_data = api_request.json()

    except Exception as e:

        return Response({

            "error": "Recharge Server Error",
            "details": str(e)

        }, status=500)

    # =====================================================
    # API STATUS
    # =====================================================

    status_value = str(
        api_data.get("STATUS")
    )

    message = api_data.get(
        "MESSAGE",
        ""
    )

    # =====================================================
    # SUCCESS
    # =====================================================

    if status_value == "1":

        # DEDUCT WALLET

        user.wallet_balance -= amount

        # CASHBACK

        cashback = (

            amount *

            Decimal(provider.cashback_percentage)

        ) / Decimal(100)

        user.wallet_balance += cashback

        user.save()

        # WALLET HISTORY

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

        # SAVE RECHARGE

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

            api_response=json.dumps(
                api_data
            ),

        )

        # CASHBACK HISTORY

        RechargeCashbackHistory.objects.create(

            recharge=recharge,

            user=user,

            cashback_percentage=provider.cashback_percentage,

            cashback_amount=cashback,

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

                    amount=income,

                )

            current_user = current_user.referred_by

            current_level += 1

        return Response({

            "status": "success",

            "message": message,

            "recharge_id": recharge.id,

            "cashback": cashback,

            "wallet_balance": str(
                user.wallet_balance
            ),

            "api_response": api_data

        })

    # =====================================================
    # FAILED
    # =====================================================

    else:

        Recharge.objects.create(

            user=user,

            provider=provider,

            mobile_number=mobile_number,

            amount=amount,

            cashback=0,

            status='failed',

            transaction_id=request_txn_id,

            api_response=json.dumps(
                api_data
            ),

        )

        return Response({

            "status": "failed",

            "message": message,

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
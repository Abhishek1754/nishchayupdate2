from django.shortcuts import render
from decimal import Decimal

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
# ==================== UI PAGES =======================
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
# ======================= APIs ========================
# =====================================================


# =========================
# ALL PROVIDERS API
# =========================

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

            "cashback_percentage": provider.cashback_percentage,

        })

    return Response(data)


# =========================
# RECHARGE API
# =========================

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

    # =========================
    # VALIDATION
    # =========================

    if not provider_id:

        return Response({

            "error": "provider_id is required"

        }, status=400)

    if not mobile_number:

        return Response({

            "error": "mobile_number is required"

        }, status=400)

    if not amount:

        return Response({

            "error": "amount is required"

        }, status=400)

    amount = Decimal(amount)

    # =========================
    # PROVIDER CHECK
    # =========================

    try:

        provider = RechargeProvider.objects.get(
            id=provider_id,
            is_active=True
        )

    except RechargeProvider.DoesNotExist:

        return Response({

            "error": "Provider not found"

        }, status=404)

    # =========================
    # CHECK WALLET
    # =========================

    if Decimal(user.wallet_balance) < amount:

        return Response({

            "error": "Insufficient wallet balance"

        }, status=400)

    # =========================
    # DEDUCT WALLET
    # =========================

    user.wallet_balance -= amount

    # =========================
    # CASHBACK CALCULATION
    # =========================

    cashback = (

        amount *

        Decimal(provider.cashback_percentage)

    ) / Decimal(100)

    # CREDIT CASHBACK

    user.wallet_balance += cashback

    user.save()

    # =========================
    # WALLET HISTORY
    # =========================

    create_wallet_transaction(

        user=user,

        transaction_type='debit',

        source='recharge',

        amount=amount,

        remark='Recharge Payment'

    )

    # =========================
    # CASHBACK HISTORY
    # =========================

    if cashback > 0:

        create_wallet_transaction(

            user=user,

            transaction_type='credit',

            source='recharge',

            amount=cashback,

            remark='Recharge Cashback'

        )

    # =========================
    # CREATE RECHARGE ENTRY
    # =========================

    recharge = Recharge.objects.create(

        user=user,

        provider=provider,

        mobile_number=mobile_number,

        amount=amount,

        cashback=cashback,

        status='success',

        transaction_id='TEMP12345',

        api_response='Recharge Success',

    )

    # =========================
    # SAVE CASHBACK HISTORY
    # =========================

    RechargeCashbackHistory.objects.create(

        recharge=recharge,

        user=user,

        cashback_percentage=provider.cashback_percentage,

        cashback_amount=cashback,

    )

    # =========================
    # LEVEL INCOME DISTRIBUTION
    # =========================

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

        # LEVEL INCOME

        income = (

            amount *

            percentage

        ) / Decimal(100)

        if income > 0:

            # CREDIT WALLET

            current_user.wallet_balance += income

            current_user.save()

            # WALLET HISTORY

            create_wallet_transaction(

                user=current_user,

                transaction_type='credit',

                source='recharge',

                amount=income,

                remark=f'Level {current_level} Recharge Income'

            )

            # SAVE LEVEL HISTORY

            RechargeLevelIncome.objects.create(

                recharge=recharge,

                user=current_user,

                from_user=user,

                level=current_level,

                percentage=percentage,

                amount=income,

            )

        # NEXT LEVEL

        current_user = current_user.referred_by

        current_level += 1

    return Response({

        "msg": "Recharge Successful",

        "recharge_id": recharge.id,

        "cashback": cashback,

    })


# =========================
# MY RECHARGES API
# =========================

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

            "amount": recharge.amount,

            "cashback": recharge.cashback,

            "status": recharge.status,

            "transaction_id": recharge.transaction_id,

            "created_at": recharge.created_at,

        })

    return Response(data)
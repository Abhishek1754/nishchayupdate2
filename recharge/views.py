from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from wallet.utils import create_wallet_transaction

from .models import (

    RechargeProvider,
    Recharge,
    RechargeLevelIncome,

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

    amount = float(
        request.data.get('amount')
    )

    try:

        provider = RechargeProvider.objects.get(
            id=provider_id
        )

    except RechargeProvider.DoesNotExist:

        return Response({

            "error": "Provider not found"

        }, status=404)

    # CHECK WALLET

    if user.wallet_balance < amount:

        return Response({

            "error": "Insufficient wallet balance"

        }, status=400)

    # DEDUCT WALLET

    user.wallet_balance -= amount

    # CASHBACK

    cashback = (

        amount *

        float(provider.cashback_percentage)

    ) / 100

    user.wallet_balance += cashback

    user.save()

    # WALLET HISTORY

    create_wallet_transaction(

        user=user,

        transaction_type='debit',

        source='recharge',

        amount=amount,

        remark='Recharge Payment'

    )

    if cashback > 0:

        create_wallet_transaction(

            user=user,

            transaction_type='credit',

            source='recharge',

            amount=cashback,

            remark='Recharge Cashback'

        )

    # CREATE RECHARGE ENTRY

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
    # LEVEL INCOME DISTRIBUTION
    # =========================

    current_user = user.referred_by

    level_percentages = [

        provider.level_1_percentage,

        provider.level_2_percentage,

        provider.level_3_percentage,

    ]

    level = 1

    for percentage in level_percentages:

        if current_user and percentage > 0:

            income = (

                amount *

                float(percentage)

            ) / 100

            current_user.wallet_balance += income

            current_user.save()

            # WALLET HISTORY

            create_wallet_transaction(

                user=current_user,

                transaction_type='credit',

                source='recharge',

                amount=income,

                remark=f'Level {level} Recharge Income'

            )

            # SAVE LEVEL INCOME

            RechargeLevelIncome.objects.create(

                recharge=recharge,

                user=current_user,

                from_user=user,

                level=level,

                percentage=percentage,

                amount=income,

            )

            current_user = current_user.referred_by

            level += 1

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

            "created_at": recharge.created_at,

        })

    return Response(data)
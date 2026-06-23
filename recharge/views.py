from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
import requests

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
    RechargeWallet,
    RechargeWalletHistory,
    AddMoneyRequest,
    RechargeCoupon,
    RechargePaymentGateway,
    RechargeWithdrawRequest

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

    coupons = RechargeCoupon.objects.filter(
        is_active=True
    )

    providers = RechargeProvider.objects.filter(
        is_active=True
    )

    gateway = RechargePaymentGateway.objects.filter(
        is_active=True
    ).first()

    context = {

        "coupons": coupons,
        "providers": providers,
        "gateway": gateway,

    }

    return render(
        request,
        'recharge/index.html',
        context
    )


def mobile_recharge(request):
    return render(request, 'recharge/mobile.html')


def recharge_payment(request):
    return render(request, 'recharge/payment/index.html')


def recharge_success(request):
    return render(request, 'recharge/success/index.html')


def transaction_history(request):
    return render(request, 'recharge/transactions/index.html')

def wallet_history_page(request):

    return render(
        request,
        'recharge/wallet_history.html'
    )


from django.db.models import Sum
from decimal import Decimal

def refer_earn(request):

    if not request.user.is_authenticated:

        return render(
            request,
            'recharge/refer/index.html'
        )

    direct_team = request.user.team_members.count()

    total_income = RechargeLevelIncome.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    today_income = RechargeLevelIncome.objects.filter(
        user=request.user,
        created_at__date=timezone.now().date()
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    recent_income = RechargeLevelIncome.objects.filter(
        user=request.user
    ).order_by('-id')[:10]

    context = {

        "referral_code":
        request.user.referral_code,

        "direct_team":
        direct_team,

        "total_income":
        total_income,

        "today_income":
        today_income,

        "recent_income":
        recent_income,

    }

    return render(
        request,
        'recharge/refer/index.html',
        context
    )


def profile_page(request):

    if not request.user.is_authenticated:

        return render(
            request,
            'recharge/profile/index.html'
        )

    wallet, created = RechargeWallet.objects.get_or_create(
        user=request.user
    )

    total_income = RechargeLevelIncome.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    total_transactions = Recharge.objects.filter(
        user=request.user
    ).count()

    context = {

        "user_obj": request.user,

        "wallet": wallet,

        "total_income": total_income,

        "total_transactions": total_transactions,

    }

    return render(

        request,

        'recharge/profile/index.html',

        context

    )


def withdraw_page(request):
    return render(request, 'recharge/withdraw/index.html')


def offers_page(request):
    return render(request, 'recharge/offers/index.html')


def notifications_page(request):
    return render(request, 'recharge/notifications/index.html')


def support_page(request):
    return render(request, 'recharge/support/index.html')

def team_page(request):

    return render(
        request,
        'recharge/team/index.html'
    )


# =====================================================
# GET WALLET
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_details(request):

    wallet, created = RechargeWallet.objects.get_or_create(
        user=request.user
    )

    return Response({

        "balance": str(wallet.balance),
        "total_added": str(wallet.total_added),
        "total_spent": str(wallet.total_spent),
        "total_cashback": str(wallet.total_cashback),

    })
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

            "id": provider.operator_code,
            "name": provider.name,
            "operator_code": provider.operator_code,
            "service_type": provider.service_type,
            "cashback_percentage": str(
                provider.cashback_percentage
            ),

            "image": (
                provider.image.url
                if provider.image
                else None
            )

        })

    return Response(data)


# =====================================================
# COUPONS
# =====================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def recharge_coupons(request):

    coupons = RechargeCoupon.objects.filter(
        is_active=True,
        expiry_date__gte=timezone.now()
    )

    data = []

    for coupon in coupons:

        data.append({

            "id": coupon.id,
            "code": coupon.code,
            "title": coupon.title,
            "description": coupon.description,
            "cashback_percentage": str(
                coupon.cashback_percentage
            ),
            "max_cashback": str(
                coupon.max_cashback
            ),
            "minimum_amount": str(
                coupon.minimum_amount
            )

        })

    return Response(data)


# =====================================================
# ADD MONEY REQUEST
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_money_request(request):

    try:

        amount = request.data.get(
            'amount'
        )

        payment_method = request.data.get(
            'payment_method'
        )

        utr_number = request.data.get(
            'utr_number'
        )

        screenshot = request.FILES.get(
            'screenshot'
        )

        add_request = AddMoneyRequest.objects.create(

            user=request.user,

            amount=Decimal(amount),

            payment_method=payment_method,

            utr_number=utr_number,

            screenshot=screenshot,

            status='pending'

        )

        return Response({

            "status": True,
            "message": "Payment submitted successfully"

        })

    except Exception as e:

        return Response({

            "status": False,
            "message": str(e)

        }, status=500)


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

        coupon_code = request.data.get(
            'coupon_code'
        )

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

        cashback_amount = Decimal("0")

        coupon_instance = None

        # =====================================================
        # USER WALLET
        # =====================================================

        wallet = None

        if request.user.is_authenticated:

            wallet, created = RechargeWallet.objects.get_or_create(
                user=request.user
            )

            if wallet.balance < Decimal(amount):

                return Response({

                    "status": False,
                    "message": "Insufficient wallet balance"

                }, status=400)

        # =====================================================
        # COUPON
        # =====================================================

        if coupon_code:

            try:

                coupon_instance = RechargeCoupon.objects.get(

                    code=coupon_code,
                    is_active=True

                )

                cashback_amount = (

                    Decimal(amount)
                    *
                    coupon_instance.cashback_percentage
                ) / Decimal("100")

                if cashback_amount > coupon_instance.max_cashback:

                    cashback_amount = (
                        coupon_instance.max_cashback
                    )

            except:

                pass

        # =====================================================
        # TXN ID
        # =====================================================

        transaction_id = str(
            uuid.uuid4()
        ).replace('-', '')[:15]

        recharge_url = (

            f"https://ultra.myfinpaypro.co.in/api/Service/Recharge2?"
            f"ApiToken={API_TOKEN}"
            f"&MobileNo={mobile_number}"
            f"&Amount={amount}"
            f"&OpId={provider.operator_code}"
            f"&RefTxnId={transaction_id}"

        )

        response = requests.get(
            recharge_url,
            timeout=30
        )

        api_data = response.json()

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

                user=request.user
                if request.user.is_authenticated
                else None,

                provider=provider,

                mobile_number=mobile_number,

                amount=Decimal(amount),

                cashback=cashback_amount,

                coupon=coupon_instance,

                status='success',

                transaction_id=transaction_id,

                operator_reference=api_data.get(
                    "OPTXNID"
                ),

                api_response=json.dumps(api_data)

            )

            # =====================================================
            # WALLET DEDUCT
            # =====================================================

            
            
            if wallet:

                wallet.balance -= Decimal(amount)

                wallet.total_spent += Decimal(amount)

                wallet.balance += cashback_amount

                wallet.total_cashback += cashback_amount

                wallet.save()

                RechargeWalletHistory.objects.create(

                    user=request.user,

                    recharge=recharge,

                    amount=Decimal(amount),

                    transaction_type='debit',

                    message='Recharge Deducted'

                )

                if cashback_amount > 0:

                    RechargeWalletHistory.objects.create(

                        user=request.user,

                        recharge=recharge,

                        amount=cashback_amount,

                        transaction_type='credit',

                        message='Recharge Cashback'

                    )

                # ============================================
                # RECHARGE LEVEL INCOME
                # ============================================

                current_user = request.user

                sponsor = current_user.referred_by

                level = 1

                while sponsor:

                    try:

                        level_setting = RechargeLevelSetting.objects.get(
                            level=level
                        )

                        income_amount = (

                            Decimal(amount)

                            * level_setting.percentage

                        ) / Decimal("100")

                        sponsor_wallet, created = RechargeWallet.objects.get_or_create(
                            user=sponsor
                        )

                        sponsor_wallet.balance += income_amount

                        sponsor_wallet.total_added += income_amount

                        sponsor_wallet.save()

                        RechargeLevelIncome.objects.create(

                            recharge=recharge,

                            user=sponsor,

                            from_user=current_user,

                            level=level,

                            percentage=level_setting.percentage,

                            amount=income_amount

                        )

                        RechargeWalletHistory.objects.create(

                            user=sponsor,

                            recharge=recharge,

                            amount=income_amount,

                            transaction_type='credit',

                            message=f'Level {level} Recharge Income'

                        )

                    except RechargeLevelSetting.DoesNotExist:

                        pass

                    sponsor = sponsor.referred_by

                    level += 1

                    if level > 20:

                        break

            return Response({

                "status": True,

                "message": api_message,

                "transaction_id": transaction_id,

                "cashback": str(cashback_amount),

                "api_response": api_data

            })


        # =====================================================
        # FAILED
        # =====================================================

        Recharge.objects.create(

            user=request.user
            if request.user.is_authenticated
            else None,

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


# =====================================================
# WALLET HISTORY
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_history(request):

    history = RechargeWalletHistory.objects.filter(
        user=request.user
    ).order_by('-id')

    data = []

    for item in history:

        data.append({

            "amount": str(item.amount),

            "transaction_type": item.transaction_type,

            "message": item.message,

            "created_at": item.created_at,

        })

    return Response(data)



# =====================================================
# WITHDRAW REQUEST
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_request(request):

    try:

        amount = Decimal(
            request.data.get('amount', 0)
        )

        withdraw_method = request.data.get(
            'withdraw_method'
        )

        account_name = request.data.get(
            'account_name'
        )

        account_details = request.data.get(
            'account_details'
        )

        if amount < Decimal('10'):

            return Response({

                "status": False,

                "message": "Minimum withdrawal is ₹10"

            }, status=400)

        wallet, created = RechargeWallet.objects.get_or_create(
            user=request.user
        )

        if wallet.balance < amount:

            return Response({

                "status": False,

                "message": "Insufficient wallet balance"

            }, status=400)

        RechargeWithdrawRequest.objects.create(

            user=request.user,

            amount=amount,

            withdraw_method=withdraw_method,

            account_name=account_name,

            account_details=account_details,

            status='pending'

        )

        return Response({

            "status": True,

            "message": "Withdrawal request submitted"

        })

    except Exception as e:

        return Response({

            "status": False,

            "message": str(e)

        }, status=500)
        
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_team(request):

    team = request.user.team_members.all()

    data = []

    for user in team:

        data.append({

            "name":
            f"{user.first_name} {user.last_name}",

            "email":
            user.email,

            "phone":
            user.phone,

            "join_date":
            user.created_at.strftime(
                "%d-%m-%Y"
            ),

        })

    return Response({

        "direct_team":
        team.count(),

        "members":
        data

    })
    





@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_plan_fetch(request):

    mobile = request.data.get("mobile")
    opcode = request.data.get("opcode")
    circle = request.data.get("circle", "")

    url = "https://api.myfinpaypro.in/api/new-mobile-plans.php"

    payload = {
    "api_key": "810393-d5eb68-51395c-be2fe0-cade53",
    "mobile": mobile,
    "opcode": opcode,
    "circle": circle
}

    try:

        response = requests.post(
            url,
            data=payload
        )
        
        print(response.text)

        return Response(response.json())

    except Exception as e:

        return Response({
            "status": False,
            "message": str(e)
        })
     

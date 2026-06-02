from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

from wallet.utils import create_wallet_transaction
from .utils import generate_daily_roi

from .models import (

    ROIPlan,
    Investment,
    WithdrawRequest,
    ROILevelIncomeHistory,

)

from accounts.models import User


# =========================
# ROI DASHBOARD
# =========================

def roi_dashboard(request):

    return render(
        request,
        'roi/index.html'
    )


# =========================
# ROI PLANS PAGE
# =========================

def roi_plans(request):

    return render(
        request,
        'roi/plans.html'
    )


# =========================
# PLAN DETAILS PAGE
# =========================

def plan_details(request):

    return render(
        request,
        'roi/plan_details.html'
    )


# =========================
# INVEST NOW PAGE
# =========================

def invest_now_page(request):

    return render(
        request,
        'roi/invest_now.html'
    )


# =========================
# PAYMENT PAGE
# =========================

def payment_page(request):

    return render(
        request,
        'roi/payment.html'
    )


# =========================
# PAYMENT SUCCESS
# =========================

def payment_success(request):

    return render(
        request,
        'roi/payment_success.html'
    )


# =========================
# MY INVESTMENT PAGE
# =========================

def my_investment(request):

    return render(
        request,
        'roi/my_investment.html'
    )


# =========================
# REFERRAL TREE
# =========================

def referral_tree(request):

    return render(
        request,
        'roi/referral_tree.html'
    )


# =========================
# TEAM INCOME
# =========================

def team_income(request):

    return render(
        request,
        'roi/team_income.html'
    )


# =========================
# PROFILE PAGE
# =========================

def profile_page(request):

    return render(
        request,
        'roi/profile.html'
    )


# =========================
# WITHDRAW PAGE
# =========================

def withdraw_page(request):

    return render(
        request,
        'roi/withdraw.html'
    )


# =========================
# WITHDRAW SUCCESS
# =========================

def withdraw_success(request):

    return render(
        request,
        'roi/withdraw_success.html'
    )


# =====================================================
# ==================== APIs ===========================
# =====================================================


# =========================
# GET ALL ROI PLANS
# =========================

@api_view(['GET'])
@permission_classes([AllowAny])
def roi_plans_api(request):

    plans = ROIPlan.objects.filter(
        is_active=True
    )

    data = []

    for plan in plans:

        data.append({

            "id": plan.id,

            "name": plan.name,

            "amount": plan.amount,

            "percentage": plan.percentage,

            "maturity_days": plan.maturity_days,

            "maturity_amount": plan.maturity_amount,

        })

    return Response(data)


# =========================
# INVEST NOW API
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def invest_now(request):

    user = request.user

    plan_id = request.data.get('plan_id')

    if not plan_id:

        return Response({

            "error": "plan_id is required"

        }, status=400)

    try:

        plan = ROIPlan.objects.get(
            id=plan_id,
            is_active=True
        )

    except ROIPlan.DoesNotExist:

        return Response({

            "error": "Plan not found"

        }, status=404)

    # =========================
    # CHECK WALLET BALANCE
    # =========================

    if float(user.wallet_balance) < float(plan.amount):

        return Response({

            "error": "Insufficient wallet balance"

        }, status=400)

    # =========================
    # DEDUCT WALLET
    # =========================

    user.wallet_balance -= float(plan.amount)

    user.save()

    # =========================
    # CREATE INVESTMENT
    # =========================

    investment = Investment.objects.create(

        user=user,

        plan=plan,

        amount=plan.amount,

    )

    # =========================
    # WALLET HISTORY
    # =========================

    create_wallet_transaction(

        user=user,

        transaction_type='debit',

        source='roi',

        amount=plan.amount,

        remark='ROI Investment Purchase'

    )

    return Response({

        "msg": "Investment successful",

        "investment_id": investment.id,

        "wallet_balance": user.wallet_balance,

    })


# =========================
# MY INVESTMENTS API
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def my_investments(request):

    investments = Investment.objects.filter(
        user=request.user
    ).order_by('-id')

    data = []

    for investment in investments:

        data.append({

            "id": investment.id,

            "plan": investment.plan.name,

            "amount": investment.amount,

            "daily_income": investment.daily_income,

            "total_earned": investment.total_earned,

            "status": investment.status,

            "start_date": investment.start_date,

            "end_date": investment.end_date,

        })

    return Response(data)


# =========================
# TEAM INCOME API
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def team_income_api(request):

    incomes = ROILevelIncomeHistory.objects.filter(
        user=request.user
    ).order_by('-id')

    data = []

    for income in incomes:

        data.append({

            "from_user": income.from_user.email,

            "level": income.level,

            "percentage": income.percentage,

            "amount": income.amount,

            "created_at": income.created_at,

        })

    return Response(data)


# =========================
# WITHDRAW REQUEST API
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def withdraw_request(request):

    user = request.user

    amount = request.data.get('amount')

    if not amount:

        return Response({

            "error": "Amount is required"

        }, status=400)

    amount = float(amount)

    # =========================
    # CHECK BALANCE
    # =========================

    if amount > float(user.wallet_balance):

        return Response({

            "error": "Insufficient wallet balance"

        }, status=400)

    # =========================
    # CREATE REQUEST
    # =========================

    WithdrawRequest.objects.create(

        user=user,

        amount=amount,

    )

    # =========================
    # WALLET HISTORY
    # =========================

    create_wallet_transaction(

        user=user,

        transaction_type='debit',

        source='withdraw',

        amount=amount,

        remark='Withdraw Request Submitted'

    )

    return Response({

        "msg": "Withdraw request submitted"

    })


# =========================
# GENERATE DAILY ROI API
# =========================

@api_view(['POST'])
def run_daily_roi(request):

    generate_daily_roi()

    return Response({

        "msg": "Daily ROI Distributed Successfully"

    })
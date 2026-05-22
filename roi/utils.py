from django.utils import timezone

from decimal import Decimal

from accounts.models import User

from .models import (

    Investment,
    DailyROIIncome,

    ROIMonthlySalaryPlan,
    ROIMonthlySalaryIncome,

)

from wallet.utils import create_wallet_transaction


# =====================================================
# GENERATE DAILY ROI
# =====================================================

def generate_daily_roi():

    investments = Investment.objects.filter(
        status='active'
    )

    for investment in investments:

        # =========================
        # CHECK MATURITY
        # =========================

        if timezone.now() >= investment.end_date:

            investment.status = 'completed'

            investment.save()

            continue

        # =========================
        # DAILY ROI AMOUNT
        # =========================

        daily_income = Decimal(
            investment.daily_income
        )

        # =========================
        # CREDIT USER WALLET
        # =========================

        user = investment.user

        user.wallet_balance += daily_income

        user.save()

        # =========================
        # UPDATE TOTAL EARNED
        # =========================

        investment.total_earned += daily_income

        investment.save()

        # =========================
        # CREATE DAILY ROI ENTRY
        # =========================

        DailyROIIncome.objects.create(

            investment=investment,

            user=user,

            amount=daily_income,

        )

        # =========================
        # CREATE WALLET HISTORY
        # =========================

        create_wallet_transaction(

            user=user,

            transaction_type='credit',

            source='roi',

            amount=daily_income,

            remark='Daily ROI Income'

        )

    return True


# =====================================================
# GET TOTAL TEAM COUNT
# =====================================================

def get_total_team_count(user):

    total = 0

    direct_users = user.team_members.all()

    for member in direct_users:

        total += 1

        total += get_total_team_count(
            member
        )

    return total


# =====================================================
# GET TOTAL TEAM BUSINESS
# =====================================================

def get_total_team_business(user):

    total_business = Decimal(0)

    direct_users = user.team_members.all()

    for member in direct_users:

        # =========================
        # MEMBER INVESTMENTS
        # =========================

        member_investments = Investment.objects.filter(
            user=member
        )

        for investment in member_investments:

            total_business += Decimal(
                investment.amount
            )

        # =========================
        # RECURSIVE TEAM BUSINESS
        # =========================

        total_business += get_total_team_business(
            member
        )

    return total_business


# =====================================================
# GENERATE MONTHLY SALARY
# =====================================================

def generate_monthly_salary():

    users = User.objects.all()

    current_month = timezone.now().month

    current_year = timezone.now().year

    for user in users:

        # =========================
        # DIRECT TEAM COUNT
        # =========================

        direct_team = user.team_members.count()

        # =========================
        # TOTAL TEAM COUNT
        # =========================

        total_team = get_total_team_count(
            user
        )

        # =========================
        # TOTAL TEAM BUSINESS
        # =========================

        total_business = get_total_team_business(
            user
        )

        # =========================
        # CHECK SALARY PLANS
        # =========================

        plans = ROIMonthlySalaryPlan.objects.filter(
            is_active=True
        )

        for plan in plans:

            if (

                direct_team >= plan.minimum_direct_team

                and

                total_team >= plan.minimum_total_team

                and

                total_business >= plan.minimum_business

                and

                total_business <= plan.maximum_business

            ):

                # =========================
                # PREVENT DUPLICATE SALARY
                # =========================

                already_exists = (

                    ROIMonthlySalaryIncome.objects.filter(

                        user=user,

                        salary_plan=plan,

                        month=current_month,

                        year=current_year

                    ).exists()

                )

                if already_exists:

                    continue

                # =========================
                # SALARY CALCULATION
                # =========================

                salary_amount = (

                    total_business *

                    Decimal(
                        plan.commission_percentage
                    )

                ) / Decimal(100)

                # =========================
                # CREDIT WALLET
                # =========================

                user.wallet_balance += salary_amount

                user.save()

                # =========================
                # CREATE SALARY HISTORY
                # =========================

                ROIMonthlySalaryIncome.objects.create(

                    user=user,

                    salary_plan=plan,

                    total_business=total_business,

                    direct_team=direct_team,

                    total_team=total_team,

                    commission_percentage=plan.commission_percentage,

                    salary_amount=salary_amount,

                    month=current_month,

                    year=current_year,

                )

                # =========================
                # WALLET HISTORY
                # =========================

                create_wallet_transaction(

                    user=user,

                    transaction_type='credit',

                    source='roi',

                    amount=salary_amount,

                    remark='ROI Monthly Salary'

                )

    return True
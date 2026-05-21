from django.utils import timezone

from .models import (

    Investment,
    DailyROIIncome,

)

from wallet.utils import create_wallet_transaction


# =========================
# GENERATE DAILY ROI
# =========================

def generate_daily_roi():

    investments = Investment.objects.filter(
        status='active'
    )

    for investment in investments:

        # CHECK MATURITY

        if timezone.now() >= investment.end_date:

            investment.status = 'completed'

            investment.save()

            continue

        # DAILY ROI AMOUNT

        daily_income = investment.daily_income

        # CREDIT USER WALLET

        user = investment.user

        user.wallet_balance += float(
            daily_income
        )

        user.save()

        # UPDATE TOTAL EARNED

        investment.total_earned += daily_income

        investment.save()

        # CREATE DAILY ROI ENTRY

        DailyROIIncome.objects.create(

            investment=investment,

            user=user,

            amount=daily_income,

        )

        # CREATE WALLET HISTORY

        create_wallet_transaction(

            user=user,

            transaction_type='credit',

            source='roi',

            amount=daily_income,

            remark='Daily ROI Income'

        )
from decimal import Decimal

from wallet.utils import create_wallet_transaction

from .models import (

    SmartSharePlan,
    SmartShareIncome,

)


# =========================
# DISTRIBUTE SMART SHARE
# =========================

def distribute_smart_share_income(user):

    """
    Distribute 5 level smart share income
    """

    # =========================
    # DETERMINE PLAN TYPE
    # =========================

    if user.is_subscribed:

        plan_type = 'paid'

    else:

        plan_type = 'free'

    # =========================
    # GET ACTIVE PLAN
    # =========================

    plan = SmartSharePlan.objects.filter(

        plan_type=plan_type,
        is_active=True

    ).first()

    if not plan:

        return

    # =========================
    # LEVEL INCOME MAP
    # =========================

    level_income_map = {

        1: plan.level_1_income,
        2: plan.level_2_income,
        3: plan.level_3_income,
        4: plan.level_4_income,
        5: plan.level_5_income,

    }

    # =========================
    # START REFERRAL CHAIN
    # =========================

    current_user = user.referred_by

    level = 1

    while current_user and level <= plan.total_levels:

        amount = Decimal(
            level_income_map.get(level, 0)
        )

        # =========================
        # CREDIT WALLET
        # =========================

        current_user.wallet_balance += amount

        current_user.save()

        # =========================
        # CREATE SMART SHARE ENTRY
        # =========================

        SmartShareIncome.objects.create(

            plan=plan,

            user=current_user,

            from_user=user,

            level=level,

            amount=amount,

        )

        # =========================
        # WALLET HISTORY
        # =========================

        create_wallet_transaction(

            user=current_user,

            transaction_type='credit',

            source='smart_share',

            amount=amount,

            remark=f'Level {level} Smart Share Income',

        )

        # =========================
        # NISHCHAY COINS
        # =========================

        if plan_type == 'paid':

            current_user.nishchay_coin += plan.coin_paid

        else:

            current_user.nishchay_coin += plan.coin_free

        current_user.save()

        # =========================
        # MOVE NEXT LEVEL
        # =========================

        current_user = current_user.referred_by

        level += 1
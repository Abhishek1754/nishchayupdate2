from decimal import Decimal

from django.utils import timezone

from wallet.utils import create_wallet_transaction

from .models import (

    SmartSharePlan,
    SmartShareIncome,

    ShopCashbackPlan,
    ShopPurchase,
    ShopDailyQueue,
    ShopChainIncome,

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

            source='referral',

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


# =====================================================
# SHOP DAILY CASHBACK ENGINE
# =====================================================

def distribute_shop_chain_cashback(

    user,
    shop,
    amount,
    order=None

):

    """
    Daily Shop Sequential Cashback Engine

    Logic:
    - Buyer gets self cashback
    - Previous users get chain cashback
    - Same day queue
    - Queue resets automatically daily
    """

    # =========================
    # GET ACTIVE PLAN
    # =========================

    plan = ShopCashbackPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    # =========================
    # SELF CASHBACK
    # =========================

    self_cashback = (

        Decimal(amount) *

        Decimal(plan.self_cashback_percentage)

    ) / Decimal(100)

    # =========================
    # CREDIT USER WALLET
    # =========================

    user.wallet_balance += self_cashback

    user.save()

    # =========================
    # WALLET TRANSACTION
    # =========================

    create_wallet_transaction(

        user=user,

        transaction_type='credit',

        source='ecommerce',

        amount=self_cashback,

        remark='Shop Self Cashback'

    )

    # =========================
    # CREATE SHOP PURCHASE
    # =========================

    purchase = ShopPurchase.objects.create(

        user=user,

        shop=shop,

        order=order,

        amount=amount,

        cashback_amount=self_cashback,

    )

    # =========================
    # TODAY DATE
    # =========================

    today = timezone.now().date()

    # =========================
    # FIND TODAY QUEUE
    # =========================

    today_queue = ShopDailyQueue.objects.filter(

        shop=shop,

        queue_date=today

    ).order_by('queue_position')

    # =========================
    # NEW POSITION
    # =========================

    queue_position = today_queue.count() + 1

    # =========================
    # ADD CURRENT USER TO QUEUE
    # =========================

    ShopDailyQueue.objects.create(

        shop=shop,

        user=user,

        purchase=purchase,

        queue_position=queue_position,

    )

    # =========================
    # PREVIOUS USERS
    # =========================

    previous_users = today_queue.order_by(
        '-queue_position'
    )[:plan.total_chain_users]

    # =========================
    # DISTRIBUTE CHAIN INCOME
    # =========================

    level = 1

    for queue_user in previous_users:

        previous_user = queue_user.user

        # =========================
        # CHAIN CASHBACK
        # =========================

        chain_amount = (

            Decimal(amount) *

            Decimal(plan.chain_cashback_percentage)

        ) / Decimal(100)

        # =========================
        # CREDIT WALLET
        # =========================

        previous_user.wallet_balance += chain_amount

        previous_user.save()

        # =========================
        # WALLET ENTRY
        # =========================

        create_wallet_transaction(

            user=previous_user,

            transaction_type='credit',

            source='referral',

            amount=chain_amount,

            remark=f'Shop Chain Cashback Level {level}'

        )

        # =========================
        # CREATE INCOME ENTRY
        # =========================

        ShopChainIncome.objects.create(

            shop=shop,

            purchase=purchase,

            user=previous_user,

            from_user=user,

            level=level,

            amount=chain_amount,

        )

        level += 1
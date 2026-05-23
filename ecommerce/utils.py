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
    ConsumerReferralPlan,
    ConsumerReferralIncome,
    StoreBoostPlan,
    StoreBoostBusiness,
    StoreBoostIncome,
    
    RegionalConnectPlan,
    RegionalFranchise,
    RegionalFranchiseShop,
    RegionalConnectIncome,

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
        
        # =====================================================
# CONSUMER REFERRAL BONUS ENGINE
# =====================================================

def distribute_consumer_referral_bonus(

    user,
    purchase_amount,
    order=None

):

    """
    Consumer Referral Bonus System

    Level 1 = 4%
    Level 2-5 = 1%
    """

    # =========================
    # GET ACTIVE PLAN
    # =========================

    plan = ConsumerReferralPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    # =========================
    # START REFERRAL CHAIN
    # =========================

    current_user = user.referred_by

    level = 1

    while current_user and level <= plan.total_levels:

        # =========================
        # DIRECT BONUS
        # =========================

        if level == 1:

            percentage = Decimal(
                plan.direct_percentage
            )

        # =========================
        # INDIRECT BONUS
        # =========================

        else:

            percentage = Decimal(
                plan.indirect_percentage
            )

        # =========================
        # CALCULATE COMMISSION
        # =========================

        commission = (

            Decimal(purchase_amount) *

            percentage

        ) / Decimal(100)

        # =========================
        # CREDIT WALLET
        # =========================

        current_user.wallet_balance += commission

        current_user.save()

        # =========================
        # WALLET TRANSACTION
        # =========================

        create_wallet_transaction(

            user=current_user,

            transaction_type='credit',

            source='referral',

            amount=commission,

            remark=f'Consumer Referral Level {level} Bonus'

        )

        # =========================
        # CREATE INCOME RECORD
        # =========================

        ConsumerReferralIncome.objects.create(

            plan=plan,

            user=current_user,

            from_user=user,

            order=order,

            level=level,

            purchase_amount=purchase_amount,

            commission_amount=commission,

        )

        # =========================
        # NEXT LEVEL
        # =========================

        current_user = current_user.referred_by

        level += 1
        
        
        # =====================================================
# STORE BOOST MONTHLY ENGINE
# =====================================================

def distribute_store_boost_income(

    user,
    shop,
    monthly_business,
    month,
    year

):

    """
    Store Boost MLM Revenue Sharing Engine
    """

    # =========================
    # GET ACTIVE PLAN
    # =========================

    plan = StoreBoostPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    # =========================
    # NISHCHAY PROFIT
    # =========================

    nishchay_profit = (

        Decimal(monthly_business) *

        Decimal(
            plan.nishchay_commission_percentage
        )

    ) / Decimal(100)

    # =========================
    # CREATE BUSINESS ENTRY
    # =========================

    business = StoreBoostBusiness.objects.create(

        user=user,

        shop=shop,

        month=month,

        year=year,

        total_business=monthly_business,

        nishchay_profit=nishchay_profit,

    )

    # =========================
    # START REFERRAL CHAIN
    # =========================

    current_user = user

    level = 1

    while (

        current_user

        and

        level <= plan.total_levels

    ):

        # =========================
        # DIRECT %
        # =========================

        if level == 1:

            percentage = Decimal(
                plan.direct_income_percentage
            )

        # =========================
        # INDIRECT %
        # =========================

        else:

            percentage = Decimal(
                plan.indirect_income_percentage
            )

        # =========================
        # COMMISSION
        # =========================

        commission = (

            nishchay_profit *

            percentage

        ) / Decimal(100)

        # =========================
        # CREDIT WALLET
        # =========================

        current_user.wallet_balance += commission

        current_user.save()

        # =========================
        # WALLET HISTORY
        # =========================

        create_wallet_transaction(

            user=current_user,

            transaction_type='credit',

            source='referral',

            amount=commission,

            remark=f'Store Boost Level {level} Income'

        )

        # =========================
        # PREVENT DUPLICATE
        # =========================

        already_exists = (

            StoreBoostIncome.objects.filter(

                business=business,

                user=current_user,

                level=level,

            ).exists()

        )

        if already_exists:

            current_user = current_user.referred_by

            level += 1

            continue

        # =========================
        # CREATE INCOME ENTRY
        # =========================

        StoreBoostIncome.objects.create(

            plan=plan,

            business=business,

            user=current_user,

            from_user=user,

            level=level,

            total_business=monthly_business,

            nishchay_profit=nishchay_profit,

            commission_percentage=percentage,

            commission_amount=commission,

            month=month,

            year=year,

        )

        # =========================
        # NEXT LEVEL
        # =========================

        current_user = current_user.referred_by

        level += 1
        
        
        # =====================================================
# GET TEAM SIZE UPTO LEVEL
# =====================================================

def get_team_size_upto_level(

    user,
    max_level,
    current_level=1

):

    if current_level > max_level:

        return 0

    total = 0

    direct_members = user.team_members.all()

    for member in direct_members:

        total += 1

        total += get_team_size_upto_level(

            member,
            max_level,
            current_level + 1

        )

    return total


# =====================================================
# REGIONAL CONNECT FRANCHISE ENGINE
# =====================================================

def distribute_regional_connect_income(

    franchise,
    total_shop_profit,
    month,
    year

):

    """
    Regional Franchise Revenue Sharing Engine
    """

    # =========================
    # GET ACTIVE PLAN
    # =========================

    plan = RegionalConnectPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    # =========================
    # TEAM ELIGIBILITY
    # =========================

    team_size = get_team_size_upto_level(

        franchise.user,
        plan.team_level_depth

    )

    if team_size < plan.minimum_team_size:

        return

    # =========================
    # NISHCHAY PROFIT
    # =========================

    nishchay_profit = (

        Decimal(total_shop_profit) *

        Decimal(
            plan.nishchay_commission_percentage
        )

    ) / Decimal(100)

    # =========================
    # FRANCHISE INCOME
    # =========================

    franchise_income = (

        nishchay_profit *

        Decimal(
            plan.franchise_income_percentage
        )

    ) / Decimal(100)

    # =========================
    # PREVENT DUPLICATE
    # =========================

    already_exists = (

        RegionalConnectIncome.objects.filter(

            franchise=franchise,

            month=month,

            year=year,

        ).exists()

    )

    if already_exists:

        return

    # =========================
    # CREDIT WALLET
    # =========================

    franchise.user.wallet_balance += franchise_income

    franchise.user.save()

    # =========================
    # WALLET HISTORY
    # =========================

    create_wallet_transaction(

        user=franchise.user,

        transaction_type='credit',

        source='referral',

        amount=franchise_income,

        remark='Regional Connect Franchise Income'

    )

    # =========================
    # CREATE INCOME ENTRY
    # =========================

    RegionalConnectIncome.objects.create(

        franchise=franchise,

        user=franchise.user,

        total_shop_profit=total_shop_profit,

        nishchay_profit=nishchay_profit,

        franchise_percentage=plan.franchise_income_percentage,

        franchise_income=franchise_income,

        month=month,

        year=year,

    )

    # =========================
    # UPDATE TEAM SIZE
    # =========================

    franchise.total_team_size = team_size

    franchise.save()
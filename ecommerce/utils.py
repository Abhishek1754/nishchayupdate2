from decimal import Decimal

from django.utils import timezone

from wallet.utils import create_wallet_transaction
from referral.models import (
    SmartShareSetting,
    SmartShareTransaction,
)

from .models import (


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

    MasterConnectPlan,
    MasterConnect,
    MasterConnectShop,
    MasterConnectIncome,
    MonthlyCouponCampaign,
    MonthlyCouponEligibility,
    MonthlyCouponUser,
    Order,

)


# =====================================================
# DISTRIBUTE SMART SHARE
# =====================================================

def distribute_smart_share_income(user):

    if user.is_subscribed:

        plan_type = 'paid'

    else:

        plan_type = 'free'

    plan = SmartShareSetting.objects.filter(

        plan_type=plan_type,
        is_active=True

    ).first()

    if not plan:

        return

    level_income_map = {

        1: plan.level_1_income,
        2: plan.level_2_income,
        3: plan.level_3_income,
        4: plan.level_4_income,
        5: plan.level_5_income,

    }

    current_user = user.referred_by

    level = 1

    while current_user and level <= plan.total_levels:

        amount = Decimal(
            level_income_map.get(level, 0)
        )

        current_user.wallet_balance += amount

        create_wallet_transaction(

            user=current_user,

            transaction_type='credit',

            source='referral',

            amount=amount,

            remark=f'Level {level} Smart Share Income',

        )

        SmartShareTransaction.objects.create(

            plan=plan,

            user=current_user,

            from_user=user,

            level=level,

            amount=amount,

        )

        if plan_type == 'paid':

            current_user.nishchay_coin += plan.coin_paid

        else:

            current_user.nishchay_coin += plan.coin_free

        current_user.save()

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

    plan = ShopCashbackPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    self_cashback = (

        Decimal(amount) *

        Decimal(plan.self_cashback_percentage)

    ) / Decimal(100)

    user.wallet_balance += self_cashback

    user.save()

    create_wallet_transaction(

        user=user,

        transaction_type='credit',

        source='ecommerce',

        amount=self_cashback,

        remark='Shop Self Cashback'

    )

    purchase = ShopPurchase.objects.create(

        user=user,

        shop=shop,

        order=order,

        amount=amount,

        cashback_amount=self_cashback,

    )

    today = timezone.now().date()

    today_queue = ShopDailyQueue.objects.filter(

        shop=shop,

        queue_date=today

    ).order_by('queue_position')

    queue_position = today_queue.count() + 1

    ShopDailyQueue.objects.create(

        shop=shop,

        user=user,

        purchase=purchase,

        queue_position=queue_position,

    )

    previous_users = today_queue.order_by(
        '-queue_position'
    )[:plan.total_chain_users]

    level = 1

    for queue_user in previous_users:

        previous_user = queue_user.user

        chain_amount = (

            Decimal(amount) *

            Decimal(plan.chain_cashback_percentage)

        ) / Decimal(100)

        previous_user.wallet_balance += chain_amount

        previous_user.save()

        create_wallet_transaction(

            user=previous_user,

            transaction_type='credit',

            source='referral',

            amount=chain_amount,

            remark=f'Shop Chain Cashback Level {level}'

        )

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

    plan = ConsumerReferralPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    current_user = user.referred_by

    level = 1

    while current_user and level <= plan.total_levels:

        if level == 1:

            percentage = Decimal(
                plan.direct_percentage
            )

        else:

            percentage = Decimal(
                plan.indirect_percentage
            )

        commission = (

            Decimal(purchase_amount) *

            percentage

        ) / Decimal(100)

        current_user.wallet_balance += commission

        current_user.save()

        create_wallet_transaction(

            user=current_user,

            transaction_type='credit',

            source='referral',

            amount=commission,

            remark=f'Consumer Referral Level {level} Bonus'

        )

        ConsumerReferralIncome.objects.create(

            plan=plan,

            user=current_user,

            from_user=user,

            order=order,

            level=level,

            purchase_amount=purchase_amount,

            commission_amount=commission,

        )

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

    plan = StoreBoostPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    nishchay_profit = (

        Decimal(monthly_business) *

        Decimal(
            plan.nishchay_commission_percentage
        )

    ) / Decimal(100)

    business = StoreBoostBusiness.objects.create(

        user=user,

        shop=shop,

        month=month,

        year=year,

        total_business=monthly_business,

        nishchay_profit=nishchay_profit,

    )

    current_user = user

    level = 1

    while current_user and level <= plan.total_levels:

        if level == 1:

            percentage = Decimal(
                plan.direct_income_percentage
            )

        else:

            percentage = Decimal(
                plan.indirect_income_percentage
            )

        commission = (

            nishchay_profit *

            percentage

        ) / Decimal(100)

        current_user.wallet_balance += commission

        current_user.save()

        create_wallet_transaction(

            user=current_user,

            transaction_type='credit',

            source='referral',

            amount=commission,

            remark=f'Store Boost Level {level} Income'

        )

        already_exists = (

            StoreBoostIncome.objects.filter(

                business=business,

                user=current_user,

                level=level,

            ).exists()

        )

        if not already_exists:

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

    plan = RegionalConnectPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    team_size = get_team_size_upto_level(

        franchise.user,
        plan.team_level_depth

    )

    if team_size < plan.minimum_team_size:

        return

    nishchay_profit = (

        Decimal(total_shop_profit) *

        Decimal(
            plan.nishchay_commission_percentage
        )

    ) / Decimal(100)

    franchise_income = (

        nishchay_profit *

        Decimal(
            plan.franchise_income_percentage
        )

    ) / Decimal(100)

    already_exists = (

        RegionalConnectIncome.objects.filter(

            franchise=franchise,

            month=month,

            year=year,

        ).exists()

    )

    if already_exists:

        return

    franchise.user.wallet_balance += franchise_income

    franchise.user.save()

    create_wallet_transaction(

        user=franchise.user,

        transaction_type='credit',

        source='referral',

        amount=franchise_income,

        remark='Regional Connect Franchise Income'

    )

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

    franchise.total_team_size = team_size

    franchise.save()


# =====================================================
# MASTER CONNECT REVENUE ENGINE
# =====================================================

def distribute_master_connect_income(

    master_connect,
    total_shop_business,
    month,
    year

):

    plan = MasterConnectPlan.objects.filter(
        is_active=True
    ).first()

    if not plan:

        return

    total_team_size = get_team_size_upto_level(

        master_connect.user,
        plan.team_level_depth

    )

    regional_connect_count = (

        RegionalFranchise.objects.filter(

            user=master_connect.user,

            status='approved',

            is_active=True

        ).count()

    )

    if (

        total_team_size < plan.minimum_team_size

        or

        regional_connect_count < plan.minimum_regional_connects

    ):

        return

    nishchay_profit = (

        Decimal(total_shop_business) *

        Decimal(
            plan.nishchay_commission_percentage
        )

    ) / Decimal(100)

    master_income = (

        nishchay_profit *

        Decimal(
            plan.master_income_percentage
        )

    ) / Decimal(100)

    already_exists = (

        MasterConnectIncome.objects.filter(

            master_connect=master_connect,

            month=month,

            year=year,

        ).exists()

    )

    if already_exists:

        return

    master_connect.user.wallet_balance += master_income

    master_connect.user.save()

    create_wallet_transaction(

        user=master_connect.user,

        transaction_type='credit',

        source='referral',

        amount=master_income,

        remark='Master Connect Income'

    )

    MasterConnectIncome.objects.create(

        master_connect=master_connect,

        user=master_connect.user,

        total_shop_business=total_shop_business,

        nishchay_profit=nishchay_profit,

        master_percentage=plan.master_income_percentage,

        master_income=master_income,

        month=month,

        year=year,

    )

    master_connect.total_team_size = total_team_size

    master_connect.total_regional_connects = regional_connect_count

    master_connect.save()
    
    # =====================================================
# MONTHLY COUPON ELIGIBILITY ENGINE
# =====================================================

def generate_monthly_coupon_eligibility(

    user,
    month,
    year

):

    """
    Dynamic Monthly Coupon Eligibility Engine
    """

    campaigns = MonthlyCouponCampaign.objects.filter(
        is_active=True
    )

    for campaign in campaigns:

        eligibility_rules = campaign.eligibilities.all()

        is_eligible = True

        for rule in eligibility_rules:

            # =========================
            # PURCHASE AMOUNT
            # =========================

            if rule.condition_type == 'purchase_amount':

                total_purchase = (

                    Order.objects.filter(

                        user=user,

                        created_at__month=month,

                        created_at__year=year

                    ).aggregate(

                        total=models.Sum('total_amount')

                    )['total']

                    or Decimal(0)

                )

                if total_purchase < rule.minimum_value:

                    is_eligible = False

                    break

            # =========================
            # ORDER COUNT
            # =========================

            elif rule.condition_type == 'order_count':

                total_orders = (

                    Order.objects.filter(

                        user=user,

                        created_at__month=month,

                        created_at__year=year

                    ).count()

                )

                if total_orders < int(rule.minimum_value):

                    is_eligible = False

                    break

            # =========================
            # SHOP PURCHASE COUNT
            # =========================

            elif rule.condition_type == 'shop_purchase_count':

                total_shop_purchase = (

                    ShopPurchase.objects.filter(

                        user=user,

                        created_at__month=month,

                        created_at__year=year

                    ).count()

                )

                if total_shop_purchase < int(rule.minimum_value):

                    is_eligible = False

                    break

            # =========================
            # WALLET BALANCE
            # =========================

            elif rule.condition_type == 'wallet_balance':

                if user.wallet_balance < rule.minimum_value:

                    is_eligible = False

                    break

            # =========================
            # ROI INVESTMENT
            # =========================

            elif rule.condition_type == 'roi_investment':

                from roi.models import Investment

                total_investment = (

                    Investment.objects.filter(

                        user=user,

                        status='active'

                    ).aggregate(

                        total=models.Sum('amount')

                    )['total']

                    or Decimal(0)

                )

                if total_investment < rule.minimum_value:

                    is_eligible = False

                    break

            # =========================
            # REGIONAL CONNECT
            # =========================

            elif rule.condition_type == 'regional_connect':

                has_regional = (

                    RegionalFranchise.objects.filter(

                        user=user,

                        status='approved',

                        is_active=True

                    ).exists()

                )

                if not has_regional:

                    is_eligible = False

                    break

            # =========================
            # MASTER CONNECT
            # =========================

            elif rule.condition_type == 'master_connect':

                has_master = (

                    MasterConnect.objects.filter(

                        user=user,

                        status='approved',

                        is_active=True

                    ).exists()

                )

                if not has_master:

                    is_eligible = False

                    break

            # =========================
            # TEAM SIZE
            # =========================

            elif rule.condition_type == 'team_size':

                team_size = get_team_size_upto_level(

                    user,
                    10

                )

                if team_size < int(rule.minimum_value):

                    is_eligible = False

                    break

        # =========================
        # CREATE ELIGIBLE USER
        # =========================

        if is_eligible:

            already_exists = (

                MonthlyCouponUser.objects.filter(

                    campaign=campaign,

                    user=user,

                    month=month,

                    year=year,

                ).exists()

            )

            if not already_exists:

                MonthlyCouponUser.objects.create(

                    campaign=campaign,

                    user=user,

                    month=month,

                    year=year,

                    status='eligible'

                )
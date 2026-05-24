from decimal import Decimal

from wallet.utils import create_wallet_transaction

from .models import (

    FoodOrder,

    GroupOrder,
    GroupOrderMember,

)


# =====================================================
# FOOD ORDER CASHBACK ENGINE
# =====================================================

def distribute_food_cashback(order):

    """
    Cashback reward after successful order
    """

    cashback_percentage = Decimal(5)

    cashback_amount = (

        Decimal(order.total_amount) *

        cashback_percentage

    ) / Decimal(100)

    user = order.user

    user.wallet_balance += cashback_amount

    user.save()

    order.cashback_amount = cashback_amount

    order.save()

    create_wallet_transaction(

        user=user,

        transaction_type='credit',

        source='ecommerce',

        amount=cashback_amount,

        remark='FUDDO Food Cashback'

    )

    return cashback_amount


# =====================================================
# GROUP ORDER CASHBACK ENGINE
# =====================================================

def distribute_group_order_cashback(group_order):

    """
    Bonus cashback for group ordering
    """

    cashback_percentage = Decimal(

        group_order.cashback_percentage
    )

    members = group_order.members.all()

    for member in members:

        cashback_amount = (

            Decimal(member.total_amount) *

            cashback_percentage

        ) / Decimal(100)

        member.user.wallet_balance += cashback_amount

        member.user.save()

        create_wallet_transaction(

            user=member.user,

            transaction_type='credit',

            source='referral',

            amount=cashback_amount,

            remark='Group Order Cashback'

        )


# =====================================================
# GROUP ORDER TOTAL UPDATE
# =====================================================

def update_group_order_total(group_order):

    """
    Update group order totals
    """

    total_amount = Decimal(0)

    total_members = group_order.members.count()

    for member in group_order.members.all():

        total_amount += Decimal(
            member.total_amount
        )

    group_order.total_amount = total_amount

    group_order.total_members = total_members

    group_order.save()

    return group_order


# =====================================================
# FOOD XP SYSTEM
# =====================================================

def give_food_xp(user, order_amount):

    """
    XP reward system
    """

    xp_points = int(

        Decimal(order_amount) / Decimal(10)

    )

    if not hasattr(user, 'food_xp'):

        return 0

    user.food_xp += xp_points

    user.save()

    return xp_points


# =====================================================
# FOOD LEVEL SYSTEM
# =====================================================

def get_foodie_level(user):

    """
    User foodie level system
    """

    if not hasattr(user, 'food_xp'):

        return "Starter"

    xp = user.food_xp

    if xp >= 50000:

        return "Food Legend"

    elif xp >= 20000:

        return "Food King"

    elif xp >= 10000:

        return "Food Master"

    elif xp >= 5000:

        return "Food Explorer"

    elif xp >= 1000:

        return "Food Lover"

    return "Starter"


# =====================================================
# DELIVERY PARTNER EARNING ENGINE
# =====================================================

def calculate_delivery_partner_earning(order):

    """
    Delivery partner earning logic
    """

    base_earning = Decimal(40)

    distance_bonus = Decimal(20)

    total_earning = (

        base_earning +

        distance_bonus

    )

    return total_earning


# =====================================================
# ORDER STATUS UPDATE ENGINE
# =====================================================

def update_order_status(

    order,
    status_value

):

    """
    Update order live status
    """

    order.status = status_value

    order.save()

    return order


# =====================================================
# GROUP ORDER SPLIT ENGINE
# =====================================================

def split_group_order_amount(

    group_order,
    total_amount

):

    """
    Equal split between members
    """

    members = group_order.members.all()

    total_members = members.count()

    if total_members == 0:

        return

    split_amount = (

        Decimal(total_amount) /

        Decimal(total_members)

    )

    for member in members:

        member.total_amount = split_amount

        member.save()

    update_group_order_total(
        group_order
    )


# =====================================================
# FUDDO REWARD MULTIPLIER
# =====================================================

def calculate_reward_multiplier(user):

    """
    Loyalty multiplier system
    """

    if not hasattr(user, 'food_xp'):

        return Decimal(1)

    xp = user.food_xp

    if xp >= 50000:

        return Decimal(2)

    elif xp >= 20000:

        return Decimal('1.75')

    elif xp >= 10000:

        return Decimal('1.50')

    elif xp >= 5000:

        return Decimal('1.25')

    return Decimal(1)
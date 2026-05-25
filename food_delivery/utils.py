from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from decimal import Decimal

from django.utils import timezone

from wallet.utils import create_wallet_transaction


# =====================================================
# CHANNEL LAYER
# =====================================================

channel_layer = get_channel_layer()


# =====================================================
# SEND LIVE ORDER UPDATE
# =====================================================

def send_order_tracking_update(

    order_id,
    status,
    latitude=None,
    longitude=None,
    eta=None

):

    """
    Send realtime order tracking updates
    """

    room_group_name = f'order_{order_id}'

    async_to_sync(

        channel_layer.group_send

    )(

        room_group_name,

        {

            'type': 'send_tracking_update',

            'status': status,

            'latitude': latitude,

            'longitude': longitude,

            'eta': eta,

        }

    )


# =====================================================
# SEND GROUP ORDER UPDATE
# =====================================================

def send_group_order_update(

    group_code,
    action,
    user,
    item=None,
    quantity=None,
    total_amount=None

):

    """
    Send realtime group order updates
    """

    room_group_name = (

        f'group_order_{group_code}'

    )

    async_to_sync(

        channel_layer.group_send

    )(

        room_group_name,

        {

            'type': 'send_group_update',

            'action': action,

            'user': user,

            'item': item,

            'quantity': quantity,

            'total_amount': str(total_amount),

        }

    )


# =====================================================
# SEND ORDER CREATED EVENT
# =====================================================

def order_created_event(order):

    """
    Trigger realtime event when order created
    """

    send_order_tracking_update(

        order_id=order.id,

        status='pending',

        eta='45 mins'

    )


# =====================================================
# SEND ORDER ACCEPTED EVENT
# =====================================================

def order_accepted_event(order):

    """
    Trigger realtime event when order accepted
    """

    send_order_tracking_update(

        order_id=order.id,

        status='accepted',

        eta='35 mins'

    )


# =====================================================
# SEND ORDER PICKED EVENT
# =====================================================

def order_picked_event(

    order,
    latitude=None,
    longitude=None

):

    """
    Trigger realtime rider pickup event
    """

    send_order_tracking_update(

        order_id=order.id,

        status='picked',

        latitude=latitude,

        longitude=longitude,

        eta='20 mins'

    )


# =====================================================
# SEND ORDER NEARBY EVENT
# =====================================================

def order_nearby_event(

    order,
    latitude=None,
    longitude=None

):

    """
    Trigger nearby delivery event
    """

    send_order_tracking_update(

        order_id=order.id,

        status='nearby',

        latitude=latitude,

        longitude=longitude,

        eta='5 mins'

    )


# =====================================================
# SEND ORDER DELIVERED EVENT
# =====================================================

def order_delivered_event(order):

    """
    Trigger delivered event
    """

    send_order_tracking_update(

        order_id=order.id,

        status='delivered',

        eta='Delivered'

    )


# =====================================================
# DISTRIBUTE FOOD CASHBACK
# =====================================================

def distribute_food_cashback(order):

    """
    Cashback system
    """

    cashback_percentage = Decimal(5)

    cashback_amount = (

        Decimal(order.total_amount)

        * cashback_percentage

    ) / Decimal(100)

    user = order.user

    user.wallet_balance += cashback_amount

    user.total_earnings += cashback_amount

    user.save()

    order.cashback_amount = cashback_amount

    order.save()

    create_wallet_transaction(

        user=user,

        transaction_type='credit',

        source='food_delivery',

        amount=cashback_amount,

        remark='FUDDO Cashback Reward'

    )

    return cashback_amount


# =====================================================
# DELIVERY PARTNER EARNING
# =====================================================

def calculate_delivery_earning(order):

    """
    Delivery earning logic
    """

    base_earning = Decimal(40)

    distance_bonus = Decimal(20)

    total_earning = (

        base_earning +

        distance_bonus

    )

    return total_earning


# =====================================================
# COMPLETE DELIVERY FLOW
# =====================================================

def complete_delivery(order):

    """
    Complete delivery process
    """

    order.status = 'delivered'

    order.delivered_at = timezone.now()

    order.save()

    # DELIVERY PARTNER

    if order.delivery_partner:

        partner = order.delivery_partner

        earning = calculate_delivery_earning(order)

        partner.total_earnings += earning

        partner.total_deliveries += 1

        partner.is_available = True

        partner.current_order = None

        partner.save()

    # CASHBACK

    distribute_food_cashback(order)

    # REALTIME EVENT

    order_delivered_event(order)

    return True
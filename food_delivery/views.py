from decimal import Decimal
import random
import string

from django.shortcuts import render
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from wallet.utils import create_wallet_transaction

from .models import (

    Restaurant,
    FoodItem,

    FoodCart,

    DeliveryAddress,

    GroupOrder,
    GroupOrderMember,

    FoodOrder,
    FoodOrderItem,

    DeliveryPartner,

    OrderTrackingLog,

)

from .serializers import (

    RestaurantSerializer,
    FoodItemSerializer,

    FoodCartSerializer,

    GroupOrderSerializer,

    FoodOrderSerializer,

    DeliveryPartnerSerializer,

    LiveTrackingSerializer,

)

# =====================================================
# REALTIME UTILITIES
# =====================================================

from .utils import (

    send_group_order_update,

    order_created_event,
    order_accepted_event,
    order_picked_event,
    order_nearby_event,
    order_delivered_event,

    complete_delivery,

)


# =====================================================
# TEMPLATE VIEWS
# =====================================================

def fuddo_intro(request):
    return render(request, 'food_delivery/fuddo_intro.html')


def location_access(request):
    return render(request, 'food_delivery/location_access.html')


def select_role(request):
    return render(request, 'food_delivery/select_role.html')


def user_login(request):
    return render(request, 'food_delivery/user_login.html')


def user_signup(request):
    return render(request, 'food_delivery/user_signup.html')


def delivery_login(request):
    return render(request, 'food_delivery/delivery_login.html')


def delivery_signup(request):
    return render(request, 'food_delivery/delivery_signup.html')


def store_login(request):
    return render(request, 'food_delivery/store_login.html')


def store_signup(request):
    return render(request, 'food_delivery/store_signup.html')


def home(request):
    return render(request, 'food_delivery/home.html')


def services(request):
    return render(request, 'food_delivery/services.html')


def restaurants(request):
    return render(request, 'food_delivery/restaurants.html')


def menu(request):
    return render(request, 'food_delivery/menu.html')


def cart(request):
    return render(request, 'food_delivery/cart.html')


def address(request):
    return render(request, 'food_delivery/address.html')


def payment(request):
    return render(request, 'food_delivery/payment.html')


def order_success(request):
    return render(request, 'food_delivery/order_success.html')


def tracking(request):
    return render(request, 'food_delivery/tracking.html')


def live_tracking(request):
    return render(request, 'food_delivery/live_tracking.html')


def delivered(request):
    return render(request, 'food_delivery/delivered.html')


def rewards(request):
    return render(request, 'food_delivery/rewards.html')


def profile(request):

    return render(
        request,
        'food_delivery/profile.html'
    )
    
def wallet(request):

    return render(
        request,
        'food_delivery/wallet.html'
    )
    
    


# =====================================================
# RESTAURANT LIST API
# =====================================================

@api_view(['GET'])
def restaurant_list_api(request):

    restaurants = Restaurant.objects.filter(
        is_active=True
    )

    serializer = RestaurantSerializer(
        restaurants,
        many=True
    )

    return Response(serializer.data)


# =====================================================
# RESTAURANT DETAIL API
# =====================================================

@api_view(['GET'])
def restaurant_detail_api(request, restaurant_id):

    try:

        restaurant = Restaurant.objects.get(
            id=restaurant_id,
            is_active=True
        )

    except Restaurant.DoesNotExist:

        return Response(
            {
                'error': 'Restaurant not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = RestaurantSerializer(restaurant)

    return Response(serializer.data)


# =====================================================
# FOOD ITEM LIST API
# =====================================================

@api_view(['GET'])
def food_item_list_api(request, restaurant_id):

    food_items = FoodItem.objects.filter(
        restaurant_id=restaurant_id,
        is_available=True
    )

    serializer = FoodItemSerializer(
        food_items,
        many=True
    )

    return Response(serializer.data)


# =====================================================
# ADD TO CART API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart_api(request):

    food_item_id = request.data.get('food_item_id')

    quantity = int(
        request.data.get('quantity', 1)
    )

    try:

        food_item = FoodItem.objects.get(
            id=food_item_id
        )

    except FoodItem.DoesNotExist:

        return Response(
            {
                'error': 'Food item not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    cart_item, created = FoodCart.objects.get_or_create(

        user=request.user,

        food_item=food_item,

        defaults={
            'quantity': quantity
        }

    )

    if not created:

        cart_item.quantity += quantity

        cart_item.save()

    serializer = FoodCartSerializer(cart_item)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


# =====================================================
# VIEW CART API
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart_api(request):

    cart_items = FoodCart.objects.filter(
        user=request.user
    )

    serializer = FoodCartSerializer(
        cart_items,
        many=True
    )

    return Response(serializer.data)


# =====================================================
# REMOVE CART ITEM API
# =====================================================

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item_api(request, cart_id):

    try:

        cart_item = FoodCart.objects.get(
            id=cart_id,
            user=request.user
        )

    except FoodCart.DoesNotExist:

        return Response(
            {
                'error': 'Cart item not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    cart_item.delete()

    return Response({
        'message': 'Cart item removed'
    })


# =====================================================
# CREATE GROUP ORDER API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group_order_api(request):

    restaurant_id = request.data.get('restaurant_id')

    title = request.data.get('title')

    cashback_percentage = Decimal(
        request.data.get('cashback_percentage', 0)
    )

    group_code = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=8
        )
    )

    expires_at = timezone.now() + timezone.timedelta(hours=2)

    group_order = GroupOrder.objects.create(

        restaurant_id=restaurant_id,

        created_by=request.user,

        title=title,

        group_code=group_code,

        cashback_percentage=cashback_percentage,

        expires_at=expires_at,

    )

    GroupOrderMember.objects.create(
        group_order=group_order,
        user=request.user
    )

    serializer = GroupOrderSerializer(group_order)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


# =====================================================
# JOIN GROUP ORDER API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_group_order_api(request):

    group_code = request.data.get('group_code')

    try:

        group_order = GroupOrder.objects.get(
            group_code=group_code,
            status='active'
        )

    except GroupOrder.DoesNotExist:

        return Response(
            {
                'error': 'Invalid group code'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    already_joined = GroupOrderMember.objects.filter(
        group_order=group_order,
        user=request.user
    ).exists()

    if already_joined:

        return Response({
            'message': 'Already joined'
        })

    GroupOrderMember.objects.create(
        group_order=group_order,
        user=request.user
    )

    group_order.total_members += 1

    group_order.save()

    # =================================================
    # REALTIME EVENT
    # =================================================

    send_group_order_update(
        group_code=group_order.group_code,
        action='joined',
        user=request.user.email
    )

    serializer = GroupOrderSerializer(group_order)

    return Response(serializer.data)


# =====================================================
# GROUP MEMBER CONTRIBUTION API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def group_member_contribution_api(request):

    group_order_id = request.data.get(
        'group_order_id'
    )

    contribution = Decimal(
        request.data.get('contribution', 0)
    )

    try:

        member = GroupOrderMember.objects.get(
            group_order_id=group_order_id,
            user=request.user
        )

    except GroupOrderMember.DoesNotExist:

        return Response(
            {
                'error': 'Group member not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    member.total_amount += contribution

    member.save()

    group_order = member.group_order

    total_amount = Decimal(0)

    for item in group_order.members.all():

        total_amount += item.total_amount

    group_order.total_amount = total_amount

    group_order.save()

    # =================================================
    # REALTIME GROUP UPDATE
    # =================================================

    send_group_order_update(
        group_code=group_order.group_code,
        action='contribution',
        user=request.user.email,
        total_amount=group_order.total_amount
    )

    serializer = GroupOrderSerializer(group_order)

    return Response(serializer.data)


# =====================================================
# CREATE FOOD ORDER API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_food_order_api(request):

    address_id = request.data.get('address_id')

    payment_method = request.data.get('payment_method')

    group_order_id = request.data.get('group_order_id')

    cart_items = FoodCart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():

        return Response(
            {
                'error': 'Cart is empty'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    restaurant = cart_items.first().food_item.restaurant

    subtotal = Decimal(0)

    for item in cart_items:

        subtotal += (
            item.food_item.price * item.quantity
        )

    delivery_charge = restaurant.delivery_charge

    cashback_amount = Decimal(0)

    total_amount = subtotal + delivery_charge

    order_number = ''.join(
        random.choices(
            string.digits,
            k=10
        )
    )

    estimated_delivery_time = (
        timezone.now() +
        timezone.timedelta(minutes=45)
    )

    order = FoodOrder.objects.create(

        user=request.user,

        restaurant=restaurant,

        delivery_address_id=address_id,

        group_order_id=group_order_id,

        order_number=order_number,

        subtotal=subtotal,

        delivery_charge=delivery_charge,

        cashback_amount=cashback_amount,

        total_amount=total_amount,

        payment_method=payment_method,

        estimated_delivery_time=estimated_delivery_time,

    )

    for item in cart_items:

        FoodOrderItem.objects.create(

            order=order,

            food_item=item.food_item,

            quantity=item.quantity,

            price=item.food_item.price,

            total_price=(
                item.food_item.price * item.quantity
            )

        )

    if payment_method == 'wallet':

        if request.user.wallet_balance < total_amount:

            return Response(
                {
                    'error': 'Insufficient wallet balance'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.wallet_balance -= total_amount

        request.user.save()

        create_wallet_transaction(
            user=request.user,
            transaction_type='debit',
            source='food_delivery',
            amount=total_amount,
            remark='FUDDO Food Order Payment'
        )

    OrderTrackingLog.objects.create(
        order=order,
        status='pending',
        note='Order placed successfully'
    )

    # =================================================
    # REALTIME EVENT
    # =================================================

    order_created_event(order)

    cart_items.delete()

    serializer = FoodOrderSerializer(order)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


# =====================================================
# ASSIGN DELIVERY PARTNER API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_delivery_partner_api(request):

    order_id = request.data.get('order_id')

    try:

        order = FoodOrder.objects.get(id=order_id)

    except FoodOrder.DoesNotExist:

        return Response(
            {
                'error': 'Order not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    partner = DeliveryPartner.objects.filter(
        status='online',
        is_available=True,
        is_verified=True
    ).first()

    if not partner:

        return Response(
            {
                'error': 'No delivery partner available'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    order.delivery_partner = partner

    order.status = 'accepted'

    order.accepted_at = timezone.now()

    order.save()

    partner.is_available = False

    partner.current_order = order

    partner.save()

    OrderTrackingLog.objects.create(
        order=order,
        status='accepted',
        note='Delivery partner assigned'
    )

    # =================================================
    # REALTIME EVENT
    # =================================================

    order_accepted_event(order)

    serializer = FoodOrderSerializer(order)

    return Response(serializer.data)


# =====================================================
# UPDATE LIVE LOCATION API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_live_location_api(request):

    order_id = request.data.get('order_id')

    latitude = request.data.get('latitude')

    longitude = request.data.get('longitude')

    try:

        order = FoodOrder.objects.get(id=order_id)

    except FoodOrder.DoesNotExist:

        return Response(
            {
                'error': 'Order not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    order.live_latitude = latitude

    order.live_longitude = longitude

    order.save()

    # =================================================
    # REALTIME EVENT
    # =================================================

    order_picked_event(
        order=order,
        latitude=latitude,
        longitude=longitude
    )

    return Response({
        'message': 'Live location updated'
    })


# =====================================================
# UPDATE ORDER STATUS API
# =====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status_api(request):

    order_id = request.data.get('order_id')

    status_value = request.data.get('status')

    try:

        order = FoodOrder.objects.get(id=order_id)

    except FoodOrder.DoesNotExist:

        return Response(
            {
                'error': 'Order not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    order.status = status_value

    if status_value == 'picked':

        order.picked_at = timezone.now()

        order_picked_event(order)

    elif status_value == 'nearby':

        order_nearby_event(order)

    elif status_value == 'delivered':

        complete_delivery(order)

    order.save()

    OrderTrackingLog.objects.create(
        order=order,
        status=status_value,
        note=f'Order status updated to {status_value}'
    )

    return Response({
        'message': 'Order status updated'
    })


# =====================================================
# LIVE TRACKING API
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def live_tracking_api(request, order_id):

    try:

        order = FoodOrder.objects.get(id=order_id)

    except FoodOrder.DoesNotExist:

        return Response(
            {
                'error': 'Order not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LiveTrackingSerializer(order)

    return Response(serializer.data)


# =====================================================
# USER FOOD ORDER LIST API
# =====================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_food_orders_api(request):

    orders = FoodOrder.objects.filter(
        user=request.user
    ).order_by('-created_at')

    serializer = FoodOrderSerializer(
        orders,
        many=True
    )

    return Response(serializer.data)
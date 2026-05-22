from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from wallet.utils import create_wallet_transaction

from .utils import (

    distribute_smart_share_income,
    distribute_shop_chain_cashback,
    distribute_consumer_referral_bonus,

)

from .models import (

    Product,
    Cart,

    Order,
    OrderItem,

    Shop,

)


# =====================================================
# ==================== UI PAGES =======================
# =====================================================

def ecommerce_dashboard(request):

    return render(
        request,
        'eccomerce/dashboard.html'
    )


def product_details(request):

    return render(
        request,
        'eccomerce/product_details.html'
    )


def cart_page(request):

    return render(
        request,
        'eccomerce/cart.html'
    )


def checkout_page(request):

    return render(
        request,
        'eccomerce/checkout.html'
    )


def place_order_page(request):

    return render(
        request,
        'eccomerce/place_order.html'
    )


def order_success_page(request):

    return render(
        request,
        'eccomerce/order_success.html'
    )


def order_tracking(request):

    return render(
        request,
        'eccomerce/order_tracking.html'
    )


def wallet_page(request):

    return render(
        request,
        'eccomerce/wallet.html'
    )


def referrals_page(request):

    return render(
        request,
        'ecommerce/referrals.html'
    )


# =====================================================
# ==================== APIs ===========================
# =====================================================


# =========================
# ALL PRODUCTS API
# =========================

@api_view(['GET'])
def all_products(request):

    products = Product.objects.filter(
        is_active=True
    )

    data = []

    for product in products:

        images = []

        for img in product.images.all():

            images.append(

                img.image.url

                if img.image else ""

            )

        data.append({

            "id": product.id,

            "name": product.name,

            "category": product.category.name if product.category else "",

            "subcategory": product.subcategory.name if product.subcategory else "",

            "child_category": product.child_category.name if product.child_category else "",

            "description": product.description,

            "price": product.price,

            "quantity": product.quantity,

            "cashback_percentage": product.cashback_percentage,

            "images": images,

        })

    return Response(data)


# =========================
# ADD TO CART API
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_to_cart(request):

    user = request.user

    product_id = request.data.get(
        'product_id'
    )

    quantity = int(

        request.data.get(
            'quantity',
            1
        )

    )

    try:

        product = Product.objects.get(
            id=product_id
        )

    except Product.DoesNotExist:

        return Response({

            "error": "Product not found"

        }, status=404)

    # CHECK STOCK

    if quantity > product.quantity:

        return Response({

            "error": "Insufficient stock"

        }, status=400)

    # ADD TO CART

    cart_item, created = Cart.objects.get_or_create(

        user=user,

        product=product,

    )

    if not created:

        cart_item.quantity += quantity

    else:

        cart_item.quantity = quantity

    cart_item.save()

    return Response({

        "msg": "Product added to cart"

    })


# =========================
# MY CART API
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def my_cart(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    data = []

    total = 0

    for item in cart_items:

        subtotal = (

            item.product.price *

            item.quantity

        )

        total += subtotal

        data.append({

            "cart_id": item.id,

            "product": item.product.name,

            "quantity": item.quantity,

            "price": item.product.price,

            "subtotal": subtotal,

        })

    return Response({

        "cart_items": data,

        "total_amount": total,

    })


# =========================
# CHECKOUT API
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def checkout(request):

    user = request.user

    payment_method = request.data.get(
        'payment_method',
        'wallet'
    )

    address = request.data.get(
        'address'
    )

    # =========================
    # SHOP ID
    # =========================

    shop_id = request.data.get(
        'shop_id'
    )

    try:

        shop = Shop.objects.get(
            id=shop_id
        )

    except Shop.DoesNotExist:

        return Response({

            "error": "Invalid shop"

        }, status=400)

    # =========================
    # USER CART
    # =========================

    cart_items = Cart.objects.filter(
        user=user
    )

    if not cart_items.exists():

        return Response({

            "error": "Cart is empty"

        }, status=400)

    total_amount = 0

    cashback_amount = 0

    # =========================
    # CALCULATE TOTAL
    # =========================

    for item in cart_items:

        subtotal = (

            item.product.price *

            item.quantity

        )

        total_amount += subtotal

        cashback = (

            subtotal *

            item.product.cashback_percentage

        ) / 100

        cashback_amount += cashback

    # =========================
    # WALLET PAYMENT
    # =========================

    if payment_method == 'wallet':

        if user.wallet_balance < total_amount:

            return Response({

                "error": "Insufficient wallet balance"

            }, status=400)

        user.wallet_balance -= float(
            total_amount
        )

    # =========================
    # PRODUCT CASHBACK
    # =========================

    user.wallet_balance += float(
        cashback_amount
    )

    user.save()

    # =========================
    # WALLET HISTORY
    # =========================

    create_wallet_transaction(

        user=user,

        transaction_type='debit',

        source='ecommerce',

        amount=total_amount,

        remark='Ecommerce Order Payment'

    )

    # =========================
    # PRODUCT CASHBACK ENTRY
    # =========================

    if cashback_amount > 0:

        create_wallet_transaction(

            user=user,

            transaction_type='credit',

            source='ecommerce',

            amount=cashback_amount,

            remark='Product Cashback'

        )

    # =========================
    # CREATE ORDER
    # =========================

    order = Order.objects.create(

        user=user,

        total_amount=total_amount,

        cashback_amount=cashback_amount,

        payment_method=payment_method,

        address=address,

    )

    # =========================
    # CREATE ORDER ITEMS
    # =========================

    for item in cart_items:

        OrderItem.objects.create(

            order=order,

            product=item.product,

            quantity=item.quantity,

            price=item.product.price,

        )

        # =========================
        # REDUCE STOCK
        # =========================

        product = item.product

        product.quantity -= item.quantity

        product.save()

    # =========================
    # SHOP DAILY CHAIN ENGINE
    # =========================

    distribute_shop_chain_cashback(

        user=user,
        shop=shop,
        amount=total_amount,
        order=order

    )

    # =========================
    # CONSUMER REFERRAL BONUS
    # =========================

    distribute_consumer_referral_bonus(

        user=user,
        purchase_amount=total_amount,
        order=order

    )

    # =========================
    # CLEAR CART
    # =========================

    cart_items.delete()

    # =========================
    # SMART SHARE DISTRIBUTION
    # =========================

    distribute_smart_share_income(user)

    return Response({

        "msg": "Order placed successfully",

        "order_id": order.id,

        "cashback_received": cashback_amount,

    })


# =========================
# MY ORDERS API
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    data = []

    for order in orders:

        items = []

        for item in order.items.all():

            items.append({

                "product": item.product.name,

                "quantity": item.quantity,

                "price": item.price,

            })

        data.append({

            "order_id": order.id,

            "total_amount": order.total_amount,

            "cashback_amount": order.cashback_amount,

            "payment_method": order.payment_method,

            "status": order.status,

            "created_at": order.created_at,

            "items": items,

        })

    return Response(data)
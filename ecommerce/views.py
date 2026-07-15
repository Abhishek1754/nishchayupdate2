from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Banner

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from accounts.models import User
from .models import Shop

from wallet.utils import create_wallet_transaction
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum
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
    Address,

    Shop,

)

from .serializers import ShopRegistrationSerializer

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status

from datetime import timedelta

from django.utils import timezone


# =====================================================
# ==================== UI PAGES =======================
# =====================================================





from django.db.models import Count


def ecommerce_dashboard(request):

    # ==========================
    # CATEGORY FILTER
    # ==========================

    category_id = request.GET.get("category")

    categories = (
    Category.objects
    .filter(is_active=True)
    .order_by("display_order")
)
    
    banner = Banner.objects.filter(
    is_active=True
).first()
    
    featured_products = (
    Product.objects
    .filter(
        is_active=True,
        is_featured=True
    )
    .select_related(
        "category",
        "subcategory",
        "child_category"
    )
    .prefetch_related("images")
)
    
    flash_products = (
    Product.objects
    .filter(
        is_active=True,
        is_flash_deal=True
    )
    .prefetch_related("images")
)
    
    trending_products = (
    Product.objects
    .filter(
        is_active=True,
        is_trending=True
    )
    .prefetch_related("images")
)
    
    products = (
    Product.objects
    .filter(is_active=True)
    .select_related(
        "category",
        "subcategory",
        "child_category"
    )
    .prefetch_related("images")
)
    

    

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    # ==========================
    # USER DATA
    # ==========================

    cart_count = 0
    notification_count = 0

    if request.user.is_authenticated:

        cart_count = (
    Cart.objects
    .filter(user=request.user)
    .aggregate(total=Sum("quantity"))["total"] or 0
)

    # ==========================
    # HOME PAGE
    # ==========================

    return render(

        request,

        "ecommerce/dashboard.html",

        {
            
    "banner": banner,

    "categories": categories,

    "products": products,

    "featured_products": featured_products,

    "flash_products": flash_products,

    "trending_products": trending_products,

    "cart_count": cart_count,

    "notification_count": notification_count,
}

    )
    
    
    

def product_details(request, id):

    product = get_object_or_404(
    Product.objects.prefetch_related("images"),
    id=id,
    is_active=True
)

    related_products = (
    Product.objects
    .filter(
        category=product.category,
        is_active=True
    )
    .exclude(id=product.id)
    .prefetch_related("images")[:4]
)

    return render(
        request,
        'ecommerce/product_details.html',
        {
            'product': product,
            'related_products': related_products
        }
    )
    
    

    


def cart_page(request):

    if not request.user.is_authenticated:

        return render(
            request,
            "ecommerce/cart.html",
            {
                "cart": [],
                "total": 0,
                "cashback": 0,
                "grand_total": 0,
                "notification_count": 0,
            }
        )

    cart = Cart.objects.filter(
        user=request.user
    )

    total = 0
    cashback = 0

    for item in cart:

        subtotal = item.product.price * item.quantity

        total += subtotal

        cashback += (

            subtotal *

            item.product.cashback_percentage

        ) / 100

    grand_total = total

    return render(

        request,

        "ecommerce/cart.html",

        {

            "cart": cart,

            "total": total,

            "cashback": cashback,

            "grand_total": grand_total,

            "notification_count": 0,

        }

    )


def checkout_page(request):

    if not request.user.is_authenticated:

        return render(
            request,
            "ecommerce/checkout.html",
            {
                "cart": [],
                "total": 0,
                "cashback": 0,
                "grand_total": 0,
            }
        )

    cart = Cart.objects.filter(
        user=request.user
    )

    total = 0
    cashback = 0

    for item in cart:

        subtotal = item.product.price * item.quantity

        total += subtotal

        cashback += (

            subtotal *

            item.product.cashback_percentage

        ) / 100
        
    addresses = Address.objects.filter(
        user=request.user).order_by(
             "-is_default",
             "-id"
        )
        
        
        
        
    return render(

    request,

        "ecommerce/checkout.html",

        {

            "cart": cart,

            "total": total,

            "cashback": cashback,

            "grand_total": total,
            
            "addresses": addresses,

        }

    )


def place_order_page(request):

    return render(
        request,
        'ecommerce/place_order.html'
    )


def order_success_page(request):

    order = Order.objects.filter(

        user=request.user

    ).order_by("-id").first()

    return render(

        request,

        "ecommerce/order_success.html",

        {

            "order": order

        }

    )


def order_tracking(request):

    order = Order.objects.filter(

        user=request.user

    ).order_by("-id").first()

    return render(

        request,

        "ecommerce/order_tracking.html",

        {

            "order": order,

            "courier": "Pending",

            "tracking_id": "Pending",

        }

    )


def wallet_page(request):

    return render(

        request,

        "ecommerce/wallet.html"

    )
    
# =====================================================
# ADDRESS PAGE
# =====================================================

# =====================================================
# ADDRESS PAGE
# =====================================================

@login_required(login_url="user_login_page")
def address_page(request):

    addresses = Address.objects.filter(
        user=request.user
    ).order_by(
        "-is_default",
        "-id"
    )

    return render(

        request,

        "ecommerce/address.html",

        {

            "addresses": addresses

        }

    )


# =====================================================
# ADD ADDRESS
# =====================================================

@login_required(login_url="user_login_page")
def add_address(request):

    if request.method == "POST":

        is_default = request.POST.get("is_default")

        if is_default:

            Address.objects.filter(
                user=request.user
            ).update(
                is_default=False
            )

        Address.objects.create(

            user=request.user,

            full_name=request.POST.get("full_name"),

            mobile_number=request.POST.get("mobile_number"),

            alternate_mobile=request.POST.get(
                "alternate_mobile"
            ),

            house_no=request.POST.get(
                "house_no"
            ),

            area=request.POST.get(
                "area"
            ),

            landmark=request.POST.get(
                "landmark"
            ),

            city=request.POST.get(
                "city"
            ),

            state=request.POST.get(
                "state"
            ),

            pincode=request.POST.get(
                "pincode"
            ),

            address_type=request.POST.get(
                "address_type"
            ),

            is_default=True if is_default else False

        )

        messages.success(

            request,

            "Address Added Successfully."

        )

        return redirect(
            "address_page"
        )

    return redirect(
        "address_page"
    )
    
    # =====================================================
# EDIT ADDRESS
# =====================================================

@login_required(login_url="user_login_page")
def edit_address(request, address_id):

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == "POST":

        address.full_name = request.POST.get("full_name")
        address.mobile_number = request.POST.get("mobile_number")
        address.alternate_mobile = request.POST.get("alternate_mobile")
        address.house_no = request.POST.get("house_no")
        address.area = request.POST.get("area")
        address.landmark = request.POST.get("landmark")
        address.city = request.POST.get("city")
        address.state = request.POST.get("state")
        address.pincode = request.POST.get("pincode")
        address.address_type = request.POST.get("address_type")

        address.save()

        messages.success(
            request,
            "Address updated successfully."
        )

        return redirect("address_page")

    return redirect("address_page")

# =====================================================
# DELETE ADDRESS
# =====================================================

@login_required(login_url="user_login_page")
def delete_address(request, address_id):

    address = get_object_or_404(

        Address,

        id=address_id,

        user=request.user

    )

    address.delete()

    messages.success(

        request,

        "Address deleted successfully."

    )

    return redirect(
        "address_page"
    )
    
    # =====================================================
# DEFAULT ADDRESS
# =====================================================

@login_required(login_url="user_login_page")
def set_default_address(request, address_id):

    Address.objects.filter(
        user=request.user
    ).update(
        is_default=False
    )

    address = get_object_or_404(

        Address,

        id=address_id,

        user=request.user

    )

    address.is_default = True

    address.save()

    messages.success(

        request,

        "Default address updated."

    )

    return redirect(
        "address_page"
    )


from accounts.models import User
from django.db.models import Sum
from ecommerce.models import ConsumerReferralIncome, ShopChainIncome

def referrals_page(request):

    team = User.objects.filter(
        referred_by=request.user
    )

    total_referrals = team.count()

    direct_income = ConsumerReferralIncome.objects.filter(
        user=request.user,
        level=1
    ).aggregate(
        total=Sum("commission_amount")
    )["total"] or 0

    level_income = ConsumerReferralIncome.objects.filter(
        user=request.user
    ).exclude(
        level=1
    ).aggregate(
        total=Sum("commission_amount")
    )["total"] or 0

    shop_income = ShopChainIncome.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    level_summary = []

    for level in range(1, 6):

        amount = ConsumerReferralIncome.objects.filter(
            user=request.user,
            level=level
        ).aggregate(
            total=Sum("commission_amount")
        )["total"] or 0

        level_summary.append({
            "level": level,
            "amount": amount
        })

    return render(
        request,
        "ecommerce/referrals.html",
        {
            "team": team,
            "total_referrals": total_referrals,
            "direct_income": direct_income,
            "level_income": level_income,
            "shop_income": shop_income,
            "level_summary": level_summary,
        }
    )
    
    # =====================================================
# MY ORDERS PAGE
# =====================================================

def my_orders_page(request):

    return render(

        request,

        "ecommerce/my_orders.html"

    )


# =====================================================
# ==================== APIs ===========================
# =====================================================



@api_view(["POST"])
def shop_register(request):

    serializer = ShopRegistrationSerializer(
        data=request.data
    )

    if not serializer.is_valid():

        return Response(

            serializer.errors,

            status=400

        )

    data = serializer.validated_data

    # =====================================
    # REFERRAL USER
    # =====================================

    referred_by = None

    referral_code = data.get(
        "referral_code"
    )

    if referral_code:

        try:

            referred_by = User.objects.get(

                referral_code=referral_code

            )

        except User.DoesNotExist:

            return Response({

                "error":
                "Invalid Referral Code"

            }, status=400)

    # =====================================
    # PLAN
    # =====================================

    subscription = data.get(
        "subscription_type"
    )

    if subscription == "premium":

        wallet = 2
        coins = 10
        amount = 299
        active = True
        plan = "PREMIUM"

    else:

        wallet = 1
        coins = 2
        amount = 0
        active = False
        plan = "FREE"

    # =====================================
    # CREATE USER
    # =====================================

    
    
    user = User.objects.create(

    username=data["owner_email"],

    first_name=data["owner_name"],

    email=data["owner_email"],

    phone=data["owner_contact"],

    state=data["state"],

    pincode=data["pincode"],

    role="shop",

    referred_by=referred_by,

    wallet_balance=wallet,

    ecommerce_wallet=wallet,

    nishchay_coin=coins,

    plan=plan,

    subscription_amount=amount,

    is_subscription_active=active,

    subscription_date=timezone.now(),

    password=make_password(
        data["password"]
    )

)
    
        # =====================================
    # CREATE SHOP
    # =====================================

    shop = Shop.objects.create(

        user=user,

        name=data["shop_name"],

        owner_name=data["owner_name"],

        shop_category=data["shop_category"],

        full_address=data["full_address"],

        state=data["state"],

        city=data["city"],

        pincode=data["pincode"],

        latitude=data.get("latitude"),

        longitude=data.get("longitude"),

        shop_contact=data["shop_contact"],

        owner_contact=data["owner_contact"],

        owner_email=data["owner_email"],

        gst_number=data.get("gst_number"),

        pan_number=data.get("pan_number"),

        business_pan=data.get("business_pan"),

        bank_name=data["bank_name"],

        account_holder=data["account_holder"],

        account_number=data["account_number"],

        ifsc_code=data["ifsc_code"],

        referral_code=data.get("referral_code"),

        subscription_type=subscription,

        subscription_amount=amount,

        is_paid=(subscription == "premium"),

        is_verified=False,

        aadhaar_front=data["aadhaar_front"],

        aadhaar_back=data["aadhaar_back"],

        pan_card=data["pan_card"],

        business_pan_file=data.get("business_pan_file"),

        shop_photo=data["shop_photo"],

    )

    # =====================================
    # GENERATE JWT TOKEN
    # =====================================

    refresh = RefreshToken.for_user(user)

    access = str(refresh.access_token)
    
    refresh_token = str(refresh)

    # =====================================
    # SUCCESS RESPONSE
    # =====================================

    return Response(

        {

            "status": True,

            "message": "Shop registered successfully.",

            "shop_id": shop.shop_id,

            "shop_name": shop.name,

            "subscription": shop.subscription_type,

            "wallet_balance": user.wallet_balance,

            "ecommerce_wallet": user.ecommerce_wallet,

            "nishchay_coin": user.nishchay_coin,

            "referral_code": user.referral_code,

            "access": access,

            "refresh": refresh_token,

        },

        status=201

    )
    
@api_view(["POST"])
def shop_login(request):

    username = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:

        return Response(
            {
                "status": False,
                "message": "Email and Password are required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:

        return Response(
            {
                "status": False,
                "message": "Invalid credentials."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if user.role != "shop":

        return Response(
            {
                "status": False,
                "message": "This account is not a shop account."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    try:

        shop = Shop.objects.get(user=user)

    except Shop.DoesNotExist:

        return Response(
            {
                "status": False,
                "message": "Shop profile not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    refresh = RefreshToken.for_user(user)

    return Response({

        "status": True,

        "message": "Login Successful",

        "access": str(refresh.access_token),

        "refresh": str(refresh),

        "shop_id": shop.shop_id,

        "shop_name": shop.name,

        "owner_name": shop.owner_name,

        "subscription": shop.subscription_type,

        "kyc_status": shop.kyc_status,

        "wallet_balance": user.wallet_balance,

        "nishchay_coin": user.nishchay_coin,

    })
    
    # =====================================================
# SHOP DASHBOARD PAGE
# =====================================================

def shop_dashboard(request):

    return render(

        request,

        "ecommerce/shop/dashboard.html"

    )
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])

def shop_dashboard_api(request):

    user = request.user

    try:

        shop = Shop.objects.get(
            user=user
        )

    except Shop.DoesNotExist:

        return Response({

            "status":False,

            "message":"Shop not found"

        })

    return Response({

        "status":True,

        "shop_name":shop.name,

        "owner_name":shop.owner_name,

        "wallet_balance":user.wallet_balance,

        "subscription":shop.subscription_type,

        "kyc_status":shop.kyc_status,

        "coins":user.nishchay_coin,

    })




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
        
    default_address = Address.objects.filter(
        user=user,
        is_default=True
        ).first()
    if default_address:
        order_address = (
             f"{default_address.full_name}, "
             f"{default_address.house_no}, "
             f"{default_address.area}, "
             f"{default_address.city}, "
             f"{default_address.state}, "
             f"{default_address.pincode}, "
             f"Mobile: {default_address.mobile_number}"
              )
        
    else:
        return Response(
            {
                "error": "Please add a default address first."
                },
            status=400
            )
    order = Order.objects.create(

    user=user,

    total_amount=total_amount,

    cashback_amount=cashback_amount,

    payment_method=payment_method,

    address=order_address,

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
        
        if product.quantity < item.quantity:
         return Response(
        { "error": f"{product.name} is out of stock."
         },
        status=400
        )
    product.quantity -= item.quantity
    product.save()




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
# =====================================================
# CASHFREE CREATE ORDER
# =====================================================

import uuid
import requests
from django.conf import settings


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_cashfree_order(request):

    user = request.user

    cart = Cart.objects.filter(user=user)

    if not cart.exists():

        return Response(
            {
                "error": "Cart is empty"
            },
            status=400
        )

    total = 0

    for item in cart:

        total += item.product.price * item.quantity

    payload = {

        "order_id": str(uuid.uuid4()).replace("-", "")[:20],

        "order_amount": float(total),

        "order_currency": "INR",

        "customer_details": {

            "customer_id": str(user.id),

            "customer_name": user.first_name,

            "customer_email": user.email,

            "customer_phone": user.phone,

        },

        "order_meta": {

            "return_url":

            settings.SITE_URL +

            "/ecommerce/cashfree-success/?order_id={order_id}"

        }

    }

    headers = {

        "x-client-id": settings.CASHFREE_APP_ID,

        "x-client-secret": settings.CASHFREE_SECRET_KEY,

        "x-api-version": "2023-08-01",

        "Content-Type": "application/json"

    }

    response = requests.post(

        settings.CASHFREE_ORDER_URL,

        json=payload,

        headers=headers

    )

    data = response.json()

    if response.status_code != 200:

        return Response(data, status=400)

    return Response({

    "payment_session_id": data.get("payment_session_id"),

    "order_id": data.get("order_id")

})
    
    # =====================================================
# CASHFREE VERIFY PAYMENT
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])

def cashfree_verify_payment(request):

    order_id = request.GET.get("order_id")

    if not order_id:

        return Response(
            {
                "error": "Order ID missing."
            },
            status=400
        )

    headers = {

        "x-client-id": settings.CASHFREE_APP_ID,

        "x-client-secret": settings.CASHFREE_SECRET_KEY,

        "x-api-version": "2023-08-01"

    }

    response = requests.get(

        f"{settings.CASHFREE_ORDER_URL}/{order_id}",

        headers=headers

    )

    data = response.json()

    if response.status_code != 200:

        return Response(data, status=400)

    if data.get("order_status") == "PAID":

        return Response({

            "status": True,

            "message": "Payment Successful",

            "cashfree": data

        })

    return Response({

        "status": False,

        "message": "Payment Pending",

        "cashfree": data

    })
from django.urls import path

from .views import (

    # UI PAGES

    ecommerce_dashboard,
    product_details,
    cart_page,
    checkout_page,
    place_order_page,
    order_success_page,
    order_tracking,
    wallet_page,
    referrals_page,
    my_orders,
    
    # SHOP APIs
    shop_dashboard,
    shop_register,
    shop_login,
    shop_dashboard_api,

    # APIs

    all_products,
    add_to_cart,
    my_cart,
    checkout,

)

urlpatterns = [

    # =====================================================
    # ==================== UI PAGES =======================
    # =====================================================

    path(
        '',
        ecommerce_dashboard,
        name='ecommerce_dashboard'
    ),
    
    path(
    'shop-dashboard/',
    shop_dashboard,
    name='shop_dashboard'
),

    path(
    'product-details/<int:id>/',
    product_details,
    name='product_details'
),

    path(
        'cart/',
        cart_page,
        name='cart_page'
    ),

    path(
        'checkout/',
        checkout_page,
        name='checkout_page'
    ),

    path(
        'place-order/',
        place_order_page,
        name='place_order_page'
    ),

    path(
        'order-success/',
        order_success_page,
        name='order_success_page'
    ),

    path(
        'order-tracking/',
        order_tracking,
        name='order_tracking'
    ),

    path(
        'wallet/',
        wallet_page,
        name='wallet_page'
    ),

    path(
        'referrals/',
        referrals_page,
        name='referrals_page'
    ),

    # =====================================================
    # ======================= APIs ========================
    # =====================================================
    
    path(
    'api/shop-register/',
    shop_register,
    name='shop_register'
),

path(
    'api/shop-login/',
    shop_login,
    name='shop_login'
),

path(
    'api/shop-dashboard/',
    shop_dashboard_api,
    name='shop_dashboard_api'
),

    path(
        'api/products/',
        all_products,
        name='all_products'
    ),

    path(
        'api/add-to-cart/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'api/my-cart/',
        my_cart,
        name='my_cart'
    ),

    path(
        'api/checkout/',
        checkout,
        name='checkout'
    ),
    
    
    path(
    'api/my-orders/',
    my_orders,
    name='my_orders'
),

]
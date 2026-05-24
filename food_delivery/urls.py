from django.urls import path

from .views import (

    fuddo_intro,
    location_access,
    select_role,

    user_login,
    user_signup,

    delivery_login,
    delivery_signup,

    store_login,
    store_signup,

    home,
    services,
    restaurants,
    menu,
    cart,
    address,
    payment,
    order_success,
    tracking,
    live_tracking,
    delivered,
    rewards,

    restaurant_list_api,
    restaurant_detail_api,

    food_item_list_api,

    add_to_cart_api,
    view_cart_api,
    remove_cart_item_api,

    create_group_order_api,
    join_group_order_api,

    create_food_order_api,
    user_food_orders_api,

)


urlpatterns = [

    # =====================================================
    # TEMPLATE ROUTES
    # =====================================================

    path(
        '',
        fuddo_intro,
        name='fuddo_intro'
    ),

    path(
        'location-access/',
        location_access,
        name='location_access'
    ),

    path(
        'select-role/',
        select_role,
        name='select_role'
    ),

    path(
        'user-login/',
        user_login,
        name='user_login'
    ),

    path(
        'user-signup/',
        user_signup,
        name='user_signup'
    ),

    path(
        'delivery-login/',
        delivery_login,
        name='delivery_login'
    ),

    path(
        'delivery-signup/',
        delivery_signup,
        name='delivery_signup'
    ),

    path(
        'store-login/',
        store_login,
        name='store_login'
    ),

    path(
        'store-signup/',
        store_signup,
        name='store_signup'
    ),

    path(
        'home/',
        home,
        name='home'
    ),

    path(
        'services/',
        services,
        name='services'
    ),

    path(
        'restaurants/',
        restaurants,
        name='restaurants'
    ),

    path(
        'menu/',
        menu,
        name='menu'
    ),

    path(
        'cart/',
        cart,
        name='cart'
    ),

    path(
        'address/',
        address,
        name='address'
    ),

    path(
        'payment/',
        payment,
        name='payment'
    ),

    path(
        'order-success/',
        order_success,
        name='order_success'
    ),

    path(
        'tracking/',
        tracking,
        name='tracking'
    ),

    path(
        'live-tracking/',
        live_tracking,
        name='live_tracking'
    ),

    path(
        'delivered/',
        delivered,
        name='delivered'
    ),

    path(
        'rewards/',
        rewards,
        name='rewards'
    ),

    # =====================================================
    # RESTAURANT APIs
    # =====================================================

    path(
        'api/restaurants/',
        restaurant_list_api,
        name='restaurant_list_api'
    ),

    path(
        'api/restaurants/<int:restaurant_id>/',
        restaurant_detail_api,
        name='restaurant_detail_api'
    ),

    # =====================================================
    # FOOD ITEM APIs
    # =====================================================

    path(
        'api/restaurants/<int:restaurant_id>/foods/',
        food_item_list_api,
        name='food_item_list_api'
    ),

    # =====================================================
    # CART APIs
    # =====================================================

    path(
        'api/cart/add/',
        add_to_cart_api,
        name='add_to_cart_api'
    ),

    path(
        'api/cart/',
        view_cart_api,
        name='view_cart_api'
    ),

    path(
        'api/cart/remove/<int:cart_id>/',
        remove_cart_item_api,
        name='remove_cart_item_api'
    ),

    # =====================================================
    # GROUP ORDER APIs
    # =====================================================

    path(
        'api/group-order/create/',
        create_group_order_api,
        name='create_group_order_api'
    ),

    path(
        'api/group-order/join/',
        join_group_order_api,
        name='join_group_order_api'
    ),

    # =====================================================
    # FOOD ORDER APIs
    # =====================================================

    path(
        'api/order/create/',
        create_food_order_api,
        name='create_food_order_api'
    ),

    path(
        'api/orders/',
        user_food_orders_api,
        name='user_food_orders_api'
    ),

]
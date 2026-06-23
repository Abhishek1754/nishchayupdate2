from django.urls import path

from .views import (

    # =====================================================
    # UI PAGES
    # =====================================================

    recharge_home,
    mobile_recharge,
    recharge_payment,
    recharge_success,
    payment_success,
    transaction_history,
    refer_earn,
    profile_page,
    withdraw_page,
    offers_page,
    notifications_page,
    support_page,
    wallet_history_page,
    withdraw_request,
    mobile_plan_fetch,
    create_cashfree_recharge_order,
    

    recharge_providers,
    do_recharge,
    my_recharges,

    wallet_details,
    wallet_history,

    add_money_request,

    recharge_coupons,
    team_page,
    my_team

)

urlpatterns = [

    # =====================================================
    # UI PAGES
    # =====================================================

    path(
        '',
        recharge_home,
        name='recharge_home'
    ),

    path(
        'mobile/',
        mobile_recharge,
        name='mobile_recharge'
    ),

    path(
        'payment/',
        recharge_payment,
        name='recharge_payment'
    ),

    path(
        'success/',
        recharge_success,
        name='recharge_success'
    ),
    
    path(
    'payment-success/',
    payment_success,
    name='payment_success'
),

    path(
        'transactions/',
        transaction_history,
        name='transaction_history'
    ),
    
    
    path(
    'wallet-history/',
    wallet_history_page,
    name='wallet_history_page'
),

    path(
        'refer/',
        refer_earn,
        name='refer_earn'
    ),

    path(
        'profile/',
        profile_page,
        name='profile_page'
    ),

    path(
        'withdraw/',
        withdraw_page,
        name='withdraw_page'
    ),

    path(
        'offers/',
        offers_page,
        name='offers_page'
    ),

    path(
        'notifications/',
        notifications_page,
        name='notifications_page'
    ),

    path(
        'support/',
        support_page,
        name='support_page'
    ),
    
    path(
    'api/withdraw/',
    withdraw_request,
    name='withdraw_request'
),
    
    path(
    'team/',
    team_page,
    name='team_page'
),
    
    path(
    'api/mobile-plans/',
    mobile_plan_fetch,
    name='mobile_plan_fetch'
),
    
    path(
    'api/create-order/',
    create_cashfree_recharge_order,
    name='create_cashfree_recharge_order'
),

    # =====================================================
    # APIs
    # =====================================================

    path(
        'api/providers/',
        recharge_providers,
        name='recharge_providers'
    ),

    path(
        'api/do-recharge/',
        do_recharge,
        name='do_recharge'
    ),

    path(
        'api/my-recharges/',
        my_recharges,
        name='my_recharges'
    ),

    # =====================================================
    # WALLET
    # =====================================================

    path(
        'api/wallet/',
        wallet_details,
        name='wallet_details'
    ),

    path(
        'api/wallet-history/',
        wallet_history,
        name='wallet_history'
    ),

    # =====================================================
    # ADD MONEY
    # =====================================================

    path(
        'api/add-money/',
        add_money_request,
        name='add_money_request'
    ),

    # =====================================================
    # COUPONS
    # =====================================================

    path(
        'api/coupons/',
        recharge_coupons,
        name='recharge_coupons'
    ),
    
    path(
    'api/team/',
    my_team,
    name='my_team'
),

]
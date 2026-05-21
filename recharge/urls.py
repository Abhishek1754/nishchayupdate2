from django.urls import path

from .views import (

    # UI PAGES

    recharge_home,
    mobile_recharge,
    recharge_payment,
    recharge_success,
    transaction_history,
    refer_earn,
    profile_page,
    withdraw_page,
    offers_page,
    notifications_page,
    support_page,

    # APIs

    recharge_providers,
    do_recharge,
    my_recharges,

)

urlpatterns = [

    # =====================================================
    # ==================== UI PAGES =======================
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
        'transactions/',
        transaction_history,
        name='transaction_history'
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

    # =====================================================
    # ======================= APIs ========================
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

]
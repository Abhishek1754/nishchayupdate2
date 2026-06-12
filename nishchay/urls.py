from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static

from ecommerce.views import (
    ecommerce_dashboard,
    product_details,
    cart_page,
    checkout_page,
    place_order_page,
    order_success_page,
    order_tracking,
    wallet_page,
    referrals_page
)

from accounts.admin import admin_site

from recharge.views import (
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
    support_page
)

from roi.views import (
    roi_dashboard,
    roi_plans,
    plan_details,
    invest_now,
    payment_page,
    payment_success,
    my_investment,
    referral_tree,
    team_income,
    profile_page,
    withdraw_page,
    withdraw_success
)

from accounts.views import (
    register,
    login,
    dashboard_view,
    dashboard_api,
    ai_karma_dashboard
)

from subscription.views import get_plan


# =====================================================
# HOMEPAGE
# =====================================================

def homepage(request):

    return render(
        request,
        'home/index.html'
    )
    
def team_page(request):

        return render(
        request,
        'home/team.html'
    )
        
def privacy_policy(request):
         return render(request, 'home/privacy-policy.html')

def terms_conditions(request):
         return render(request, 'home/terms-and-conditions.html')

def refund_policy(request):
    return render(request, 'home/refund-policy.html')

def shipping_policy(request):

    return render(
        request,
        'home/shipping-policy.html'
    )


# =====================================================
# URL PATTERNS
# =====================================================

urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        homepage,
        name='home'
    ),
    
    path(
    'team/',
    team_page,
    name='team'
),

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        'dashboard/',
        dashboard_view,
        name='dashboard'
    ),

    # =====================================================
    # AI KARMA
    # =====================================================

    path(
        'ai-karma/',
        ai_karma_dashboard,
        name='ai_karma'
    ),

    # =====================================================
    # CUSTOM ADMIN
    # =====================================================

    path(
        'admin/',
        admin_site.urls
    ),

    # =====================================================
    # APIs
    # =====================================================

    path(
        'api/register/',
        register
    ),

    path(
        'api/login/',
        login
    ),

    path(
        'api/subscription/',
        get_plan
    ),

    path(
        'api/dashboard/',
        dashboard_api,
        name='dashboard_api'
    ),
    
    path(
    'privacy-policy/',
    privacy_policy,
    name='privacy_policy'
),

path(
    'terms-and-conditions/',
    terms_conditions,
    name='terms_conditions'
),

path(
    'refund-policy/',
    refund_policy,
    name='refund_policy'
),

path(
    'shipping-policy/',
    shipping_policy,
    name='shipping_policy'
),


    
    

    # =====================================================
    # APPS
    # =====================================================

    path(
        '',
        include('accounts.urls')
    ),

    path(
        'recharge/',
        include('recharge.urls')
    ),

    path(
        'roi/',
        include('roi.urls')
    ),

    path(
        'ecommerce/',
        include('ecommerce.urls')
    ),

    path(
        'food/',
        include('food_delivery.urls')
    ),

]

# =====================================================
# MEDIA FILES
# =====================================================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
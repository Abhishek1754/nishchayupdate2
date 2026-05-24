from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
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
from recharge.views import recharge_payment
from roi.views import roi_dashboard,roi_plans,plan_details,invest_now,payment_page,payment_success,my_investment,referral_tree,team_income,profile_page,withdraw_page,withdraw_success
from accounts.views import (
    register,
    login,
    dashboard_view,
    dashboard_api,
    ai_karma_dashboard
)




from subscription.views import get_plan
from recharge.views import recharge_home, mobile_recharge, recharge_payment, recharge_success,transaction_history,refer_earn,profile_page,withdraw_page,offers_page,notifications_page,support_page

# HOMEPAGE VIEW
def homepage(request):
    return render(request, 'home/index.html')


urlpatterns = [

    # HOMEPAGE
   path('', homepage, name='home'),

    # SUPER ADMIN DASHBOARD
    path('dashboard/', dashboard_view, name='dashboard'),

    # AI KARMA
    path('ai-karma/', ai_karma_dashboard, name='ai_karma'),

    # CUSTOM ADMIN
    path('admin/', admin_site.urls),

    # APIs
    path('api/register/', register),
    path('api/login/', login),
    path('api/subscription/', get_plan),
    path('api/dashboard/', dashboard_api, name='dashboard_api'),

    # ACCOUNTS
    path('', include('accounts.urls')),

    # RECHARGE
   path('recharge/', include('recharge.urls')),
    path('roi/', include('roi.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('food/', include('food_delivery.urls')),
    
]
        
      
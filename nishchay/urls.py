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



from food_delivery.views import (
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
        
        path('food/', fuddo_intro, name='fuddo_intro'),
        path(
    'food/location/',
    location_access,
    name='location_access'
),
   path('food/', fuddo_intro),

path('food/location/', location_access),

path('food/select-role/', select_role),

path('food/user-login/', user_login),

path('food/user-signup/', user_signup),

path('food/delivery-login/', delivery_login),

path('food/delivery-signup/', delivery_signup),

path('food/store-login/', store_login),

path('food/store-signup/', store_signup),

path('food/home/', home),

path('food/services/', services),

path('food/restaurants/', restaurants),

path('food/menu/', menu),

path('food/cart/', cart),

path('food/address/', address),

path('food/payment/', payment),

path('food/order-confirmation/', order_success),

path('food/order-tracking/', tracking),

path('food/live-tracking/', live_tracking),

path('food/delivered/', delivered),

path('food/rewards/', rewards),
]
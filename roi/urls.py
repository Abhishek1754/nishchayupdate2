from django.urls import path

from .views import (

    roi_dashboard,
    roi_plans,
     
     
    plan_details,
    invest_now_page,
    payment_page,
    payment_success,
    my_investment,
    referral_tree,
    team_income,
    profile_page,
    withdraw_page,
    withdraw_success,

    roi_plans_api,
    invest_now,
    my_investments,
    withdraw_request,
    run_daily_roi,
    team_income_api,

)

urlpatterns = [

    # =========================
    # ROI PAGES
    # =========================

    path(
        '',
        roi_dashboard,
        name='roi_dashboard'
    ),

    path(
        'plans/',
        roi_plans,
        name='roi_plans'
    ),

    path(
        'plan-details/',
        plan_details,
        name='plan_details'
    ),

    path(
        'invest-now/',
        invest_now_page,
        name='invest_now_page'
    ),

    path(
        'payment/',
        payment_page,
        name='payment_page'
    ),

    path(
        'payment-success/',
        payment_success,
        name='payment_success'
    ),

    path(
        'my-investment/',
        my_investment,
        name='my_investment'
    ),

    path(
        'referral-tree/',
        referral_tree,
        name='referral_tree'
    ),

    path(
        'team-income/',
        team_income,
        name='team_income'
    ),

    path(
        'profile/',
        profile_page,
        name='profile'
    ),

    path(
        'withdraw/',
        withdraw_page,
        name='withdraw'
    ),

    path(
        'withdraw-success/',
        withdraw_success,
        name='withdraw_success'
    ),

    # =========================
    # ROI APIs
    # =========================

    path(
        'api/plans/',
        roi_plans_api,
        name='roi_plans_api'
    ),

    path(
        'api/invest/',
        invest_now,
        name='invest_now'
    ),

    path(
        'api/my-investments/',
        my_investments,
        name='my_investments'
    ),

    path(
        'api/withdraw/',
        withdraw_request,
        name='withdraw_request'
    ),
    
    path(
    'api/run-daily-roi/',
    run_daily_roi,
    name='run_daily_roi'
),
    
    path(
    'api/team-income/',
    team_income_api,
    name='team_income_api'
),

]
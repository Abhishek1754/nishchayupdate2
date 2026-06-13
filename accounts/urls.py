from django.urls import path

from .views import (

    home,

    register,
    login,
    profile,

    dashboard_view,
    dashboard_api,

    ai_karma_dashboard,

    user_login_page,
    user_register_page,
    forgot_password_page,
    verify_otp_page,
    reset_password_page,
    send_reset_otp,
    verify_reset_otp,
    reset_password,

)

urlpatterns = [

    path('', home, name='home'),

    # FRONTEND PAGES

    path(
        'login/',
        user_login_page,
        name='user_login_page'
    ),

    path(
        'register/',
        user_register_page,
        name='user_register_page'
    ),

    # AUTH APIs

    path(
        'api/register/',
        register,
        name='register'
    ),

    path(
        'api/login/',
        login,
        name='login'
    ),

    path(
        'api/profile/',
        profile,
        name='profile'
    ),

    # DASHBOARD

    path(
        'dashboard/',
        dashboard_view,
        name='dashboard'
    ),

    path(
        'api/dashboard/',
        dashboard_api,
        name='dashboard_api'
    ),

    # AI KARMA

    path(
        'ai-karma/',
        ai_karma_dashboard,
        name='ai_karma'
    ),
    
    path(
    'forgot-password/',
    forgot_password_page,
    name='forgot_password'
),

path(
    'verify-otp/',
    verify_otp_page,
    name='verify_otp'
),

path(
    'reset-password/',
    reset_password_page,
    name='reset_password'
),

path(

    'api/send-reset-otp/',

    send_reset_otp,

    name='send_reset_otp'

),

path(

    'api/verify-reset-otp/',

    verify_reset_otp,

    name='verify_reset_otp'

),

path(

    'api/reset-password/',

    reset_password,

    name='reset_password'

),


    
    

]
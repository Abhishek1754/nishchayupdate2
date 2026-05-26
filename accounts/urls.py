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

]
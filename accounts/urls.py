from django.urls import path

from .views import (

    home,

    register,
    login,
    profile,

    dashboard_view,
    dashboard_api,

    ai_karma_dashboard,

)

urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        '',
        home,
        name='home'
    ),

    # =========================
    # AUTH APIs
    # =========================

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

    # =========================
    # DASHBOARD
    # =========================

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

    # =========================
    # AI KARMA
    # =========================

    path(
        'ai-karma/',
        ai_karma_dashboard,
        name='ai_karma'
    ),

]
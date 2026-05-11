from django.urls import path
from django.shortcuts import redirect
from accounts.admin import admin_site

# ✅ IMPORT FIXED
from accounts.views import register, login, dashboard_view, dashboard_api
from subscription.views import get_plan
from accounts.views import ai_karma_dashboard


urlpatterns = [
    # ✅ Redirect root to dashboard
    path('', lambda request: redirect('/dashboard/')),

    # ✅ Custom Admin
    path('admin/', admin_site.urls),

    # ✅ Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    # ✅ APIs
    path('api/register/', register),
    path('api/login/', login),
    path('api/subscription/', get_plan),

    # ✅ REAL-TIME DASHBOARD API
    path('api/dashboard/', dashboard_api, name='dashboard_api'),
    path('ai-karma/', ai_karma_dashboard, name='ai_karma'),
]
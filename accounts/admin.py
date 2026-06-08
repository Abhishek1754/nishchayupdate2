
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
import json

from .models import User
from ecommerce.models import Product
from roi.models import ROIPlan, Investment


class NishchayAdminSite(AdminSite):
    site_header = "Nishchay Admin Panel"
    site_title = "Nishchay"
    index_title = "Control Center"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # =======================
        # ✅ BASIC STATS
        # =======================
        extra_context['total_users'] = User.objects.count()

        extra_context['total_wallet'] = User.objects.aggregate(
            total=Sum('wallet_balance')
        )['total'] or 0

        extra_context['total_roi'] = ROIPlan.objects.count()
        extra_context['total_products'] = Product.objects.count()

        # =======================
        # 📊 USER GROWTH CHART
        # =======================
        last_7_days = timezone.now() - timedelta(days=7)

        users_per_day = (
            User.objects
            .filter(date_joined__gte=last_7_days)
            .annotate(date=TruncDate('date_joined'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        chart_labels = []
        chart_data = []

        for item in users_per_day:
            chart_labels.append(str(item['date']))
            chart_data.append(item['count'])

        extra_context['chart_labels'] = json.dumps(chart_labels)
        extra_context['chart_data'] = json.dumps(chart_data)

        # =======================
        # 📊 EARNINGS CHART
        # =======================
        earnings_data = (
            Investment.objects
            .annotate(date=TruncDate('created_at'))  # ⚠️ change to created_at if available
            .values('date')
            .annotate(total=Sum('amount'))
            .order_by('date')
        )

        earning_labels = []
        roi_data = []
        wallet_data = []

        for item in earnings_data:
            total = item['total'] or 0

            earning_labels.append(str(item['date']))
            roi_data.append(total)
            wallet_data.append(total * 0.1)  # example logic

        extra_context['earning_labels'] = json.dumps(earning_labels)
        extra_context['roi_data'] = json.dumps(roi_data)
        extra_context['wallet_data'] = json.dumps(wallet_data)

        return super().index(request, extra_context)


# =======================
# ✅ CUSTOM ADMIN INSTANCE
# =======================
admin_site = NishchayAdminSite(name='nishchay_admin')


# =======================
# ✅ USER ADMIN
# =======================
@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'email',

        'phone',

        'plan',

        'wallet_balance',

        'nishchay_coin'

    )

    search_fields = (

        'email',

        'phone'

    )

    list_filter = (

        'plan',

        'role',

        'is_verified',

        'is_blocked',

        'is_subscription_active'

    )
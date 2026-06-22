
from django.contrib import admin
from accounts.admin import admin_site
from .models import SubscriptionPlan, UserSubscription


# =====================================================
# SUBSCRIPTION PLAN
# =====================================================

@admin.register(SubscriptionPlan, site=admin_site)
class SubscriptionPlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'name',

        'price',

        'reward_amount',

        'reward_coin',

        'validity_days',

        'is_active'

    )

    list_filter = (

        'is_active',

    )

    search_fields = (

        'name',

    )


# =====================================================
# USER SUBSCRIPTION
# =====================================================

@admin.register(UserSubscription, site=admin_site)
class UserSubscriptionAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'user',

        'plan',

        'amount',

        'start_date',

        'expiry_date',

        'status'

    )

    list_filter = (

        'status',

    )

    search_fields = (

        'user__email',

    )

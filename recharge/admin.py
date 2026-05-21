from django.contrib import admin

from accounts.admin import admin_site

from .models import (

    Recharge,
    RechargeProvider,
    RechargeLevelIncome,
    RechargeLevelSetting,
    RechargeCashbackHistory,

)


# =====================================================
# RECHARGE PROVIDER ADMIN
# =====================================================

@admin.register(RechargeProvider, site=admin_site)
class RechargeProviderAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'service_type',
        'cashback_percentage',
        'is_active',
        'created_at',

    )

    search_fields = (

        'name',

    )

    list_filter = (

        'service_type',
        'is_active',

    )


# =====================================================
# RECHARGE LEVEL SETTINGS ADMIN
# =====================================================

@admin.register(RechargeLevelSetting, site=admin_site)
class RechargeLevelSettingAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'level',
        'percentage',
        'created_at',

    )

    search_fields = (

        'level',

    )


# =====================================================
# RECHARGE ADMIN
# =====================================================

@admin.register(Recharge, site=admin_site)
class RechargeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'provider',
        'mobile_number',
        'amount',
        'cashback',
        'status',
        'transaction_id',
        'created_at',

    )

    search_fields = (

        'user__email',
        'mobile_number',
        'transaction_id',

    )

    list_filter = (

        'status',
        'provider',

    )


# =====================================================
# RECHARGE LEVEL INCOME ADMIN
# =====================================================

@admin.register(RechargeLevelIncome, site=admin_site)
class RechargeLevelIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'from_user',
        'level',
        'percentage',
        'amount',
        'created_at',

    )

    search_fields = (

        'user__email',
        'from_user__email',

    )

    list_filter = (

        'level',

    )


# =====================================================
# RECHARGE CASHBACK HISTORY ADMIN
# =====================================================

@admin.register(RechargeCashbackHistory, site=admin_site)
class RechargeCashbackHistoryAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'cashback_percentage',
        'cashback_amount',
        'created_at',

    )

    search_fields = (

        'user__email',

    )
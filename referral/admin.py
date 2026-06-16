from django.contrib import admin

from accounts.admin import admin_site

from .models import (

    SmartShareSetting,
    SmartShareTransaction,

)

@admin.register(SmartShareSetting, site=admin_site)
class SmartShareSettingAdmin(admin.ModelAdmin):

    list_display = (

        'plan_type',

        'level',

        'rupee_reward',

        'coin_reward',

        'is_active',

    )
    
@admin.register(SmartShareTransaction, site=admin_site)
class SmartShareTransactionAdmin(admin.ModelAdmin):

    list_display = (

        'receiver',

        'trigger_user',

        'level',

        'rupee_amount',

        'coin_amount',

        'created_at',

    )
from django.contrib import admin

from accounts.admin import admin_site

from .models import (

    Recharge,
    RechargeProvider,
    RechargeLevelIncome,
    RechargeLevelSetting,
    RechargeCashbackHistory,

    RechargeWallet,
    RechargeWalletHistory,

    RechargeCoupon,

    AddMoneyRequest,

    RechargePaymentGateway,
    
    RechargeWithdrawRequest,

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
        'operator_code',
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


# =====================================================
# RECHARGE WALLET ADMIN
# =====================================================

@admin.register(RechargeWallet, site=admin_site)
class RechargeWalletAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'balance',
        'total_added',
        'total_spent',
        'total_cashback',
        'updated_at',

    )


# =====================================================
# WALLET HISTORY ADMIN
# =====================================================

@admin.register(RechargeWalletHistory, site=admin_site)
class RechargeWalletHistoryAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'transaction_type',
        'amount',
        'message',
        'created_at',

    )

    search_fields = (

        'message',

    )


# =====================================================
# RECHARGE COUPON ADMIN
# =====================================================

@admin.register(RechargeCoupon, site=admin_site)
class RechargeCouponAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'code',
        'title',
        'cashback_percentage',
        'max_cashback',
        'minimum_amount',
        'is_active',
        'expiry_date',

    )


# =====================================================
# PAYMENT GATEWAY ADMIN
# =====================================================

@admin.register(RechargePaymentGateway, site=admin_site)
class RechargePaymentGatewayAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'upi_id',
        'account_name',
        'bank_name',
        'is_active',

    )


# =====================================================
# ADD MONEY REQUEST ADMIN
# =====================================================

@admin.register(AddMoneyRequest, site=admin_site)
class AddMoneyRequestAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'amount',
        'payment_method',
        'utr_number',
        'status',
        'created_at',

    )

    actions = [

        'approve_requests',

    ]

    def approve_requests(
        self,
        request,
        queryset
    ):

        for obj in queryset:

            if obj.status != 'approved':

                wallet, created = RechargeWallet.objects.get_or_create(
                    user=obj.user
                )

                wallet.balance += obj.amount

                wallet.total_added += obj.amount

                wallet.save()

                RechargeWalletHistory.objects.create(

                    user=obj.user,

                    amount=obj.amount,

                    transaction_type='credit',

                    message='Wallet Topup Approved'

                )

                obj.status = 'approved'

                obj.save()

    approve_requests.short_description = "Approve selected requests"
    
    
    # =====================================================
# WITHDRAW REQUEST ADMIN
# =====================================================

@admin.register(RechargeWithdrawRequest, site=admin_site)
class RechargeWithdrawRequestAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'amount',
        'withdraw_method',
        'account_name',
        'status',
        'created_at',

    )

    list_filter = (

        'status',
        'withdraw_method',

    )

    search_fields = (

        'account_name',
        'account_details',

    )

    actions = [

        'approve_withdrawals',

    ]

    def approve_withdrawals(
        self,
        request,
        queryset
    ):

        for obj in queryset:

            if obj.status == 'pending':

                wallet, created = RechargeWallet.objects.get_or_create(
                    user=obj.user
                )

                if wallet.balance >= obj.amount:

                    wallet.balance -= obj.amount

                    wallet.save()

                    RechargeWalletHistory.objects.create(

                        user=obj.user,

                        amount=obj.amount,

                        transaction_type='debit',

                        message='Withdrawal Approved'

                    )

                    obj.status = 'approved'

                    obj.save()

    approve_withdrawals.short_description = (
        "Approve selected withdrawals"
    )
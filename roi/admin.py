from django.contrib import admin
from django.utils import timezone

from accounts.admin import admin_site

from wallet.utils import create_wallet_transaction

from .models import (

    ROIPlan,
    Investment,
    DailyROIIncome,
    WithdrawRequest,

)


# =========================
# ROI PLAN ADMIN
# =========================

@admin.register(ROIPlan, site=admin_site)
class ROIPlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'amount',
        'percentage',
        'maturity_days',
        'maturity_amount',
        'level_income_percentage',
        'is_active',

    )

    search_fields = (

        'name',

    )

    list_filter = (

        'is_active',

    )


# =========================
# INVESTMENT ADMIN
# =========================

@admin.register(Investment, site=admin_site)
class InvestmentAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'plan',
        'amount',
        'daily_income',
        'total_earned',
        'status',
        'created_at',

    )

    search_fields = (

        'user__email',

    )

    list_filter = (

        'status',

    )


# =========================
# DAILY ROI ADMIN
# =========================

@admin.register(DailyROIIncome, site=admin_site)
class DailyROIIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'investment',
        'amount',
        'created_at',

    )

    search_fields = (

        'user__email',

    )


# =========================
# WITHDRAW REQUEST ADMIN
# =========================

@admin.register(WithdrawRequest, site=admin_site)
class WithdrawRequestAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'amount',
        'wallet_type',
        'status',
        'withdraw_available_date',
        'created_at',

    )

    search_fields = (

        'user__email',

    )

    list_filter = (

        'status',

    )

    actions = [

        'approve_withdraw',

        'reject_withdraw',

    ]

    # =========================
    # APPROVE WITHDRAW
    # =========================

    def approve_withdraw(

        self,
        request,
        queryset

    ):

        for withdraw in queryset:

            if withdraw.status == 'pending':

                user = withdraw.user

                # CHECK BALANCE

                if user.wallet_balance >= withdraw.amount:

                    # DEDUCT WALLET

                    user.wallet_balance -= float(
                        withdraw.amount
                    )

                    user.save()

                    # UPDATE STATUS

                    withdraw.status = 'approved'

                    withdraw.approved_at = timezone.now()

                    withdraw.save()

                    # WALLET HISTORY

                    create_wallet_transaction(

                        user=user,

                        transaction_type='debit',

                        source='withdraw',

                        amount=withdraw.amount,

                        remark='Withdraw Approved'

                    )

    approve_withdraw.short_description = (

        "Approve Selected Withdraw Requests"

    )

    # =========================
    # REJECT WITHDRAW
    # =========================

    def reject_withdraw(

        self,
        request,
        queryset

    ):

        queryset.update(
            status='rejected'
        )

    reject_withdraw.short_description = (

        "Reject Selected Withdraw Requests"

    )
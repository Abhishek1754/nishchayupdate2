from django.contrib import admin

from .models import WalletTransaction


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'transaction_type',
        'source',
        'amount',
        'balance_after',
        'created_at',

    )

    search_fields = (

        'user__email',

    )

    list_filter = (

        'transaction_type',
        'source',

    )
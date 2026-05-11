from django.contrib import admin
from accounts.admin import admin_site
from .models import WalletTransaction


@admin.register(WalletTransaction, site=admin_site)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'type')
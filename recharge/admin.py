from django.contrib import admin
from accounts.admin import admin_site
from .models import Recharge


@admin.register(Recharge, site=admin_site)
class RechargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'cashback')
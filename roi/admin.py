from django.contrib import admin
from accounts.admin import admin_site
from .models import ROIPlan, Investment


@admin.register(ROIPlan, site=admin_site)
class ROIPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'percentage')


@admin.register(Investment, site=admin_site)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'amount')
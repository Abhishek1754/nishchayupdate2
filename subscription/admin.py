from django.contrib import admin
from accounts.admin import admin_site
from .models import SubscriptionPlan


@admin.register(SubscriptionPlan, site=admin_site)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'days_from', 'days_to')
from django.contrib import admin
from accounts.admin import admin_site
from .models import Astrologer


@admin.register(Astrologer, site=admin_site)
class AstrologerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_per_min')
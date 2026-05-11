from django.contrib import admin
from accounts.admin import admin_site
from .models import Job


@admin.register(Job, site=admin_site)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company')
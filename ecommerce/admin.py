from django.contrib import admin
from accounts.admin import admin_site
from .models import Category, Product, Shop


@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity')


@admin.register(Shop, site=admin_site)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'is_paid')
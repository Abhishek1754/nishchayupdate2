from django.contrib import admin

from accounts.admin import admin_site

from .models import (

    Category,
    SubCategory,

    Product,
    ProductImage,

    Shop,

    Cart,

    Order,
    OrderItem,

)


# =========================
# PRODUCT IMAGE INLINE
# =========================

class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 1

    max_num = 4


# =========================
# CATEGORY ADMIN
# =========================

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'created_at',

    )

    search_fields = (

        'name',

    )


# =========================
# SUB CATEGORY ADMIN
# =========================

@admin.register(SubCategory, site=admin_site)
class SubCategoryAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'category',
        'created_at',

    )

    search_fields = (

        'name',

    )

    list_filter = (

        'category',

    )


# =========================
# PRODUCT ADMIN
# =========================

@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'category',
        'subcategory',
        'price',
        'quantity',
        'cashback_percentage',
        'is_active',

    )

    search_fields = (

        'name',
        'sku',

    )

    list_filter = (

        'category',
        'subcategory',
        'is_active',

    )

    inlines = [

        ProductImageInline,

    ]


# =========================
# SHOP ADMIN
# =========================

@admin.register(Shop, site=admin_site)
class ShopAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'user',
        'gst_number',
        'pan_number',
        'is_paid',

    )

    search_fields = (

        'name',
        'user__email',

    )


# =========================
# CART ADMIN
# =========================

@admin.register(Cart, site=admin_site)
class CartAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'product',
        'quantity',
        'created_at',

    )

    search_fields = (

        'user__email',

    )


# =========================
# ORDER ITEM INLINE
# =========================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0


# =========================
# ORDER ADMIN
# =========================

@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'total_amount',
        'cashback_amount',
        'payment_method',
        'status',
        'created_at',

    )

    search_fields = (

        'user__email',

    )

    list_filter = (

        'status',
        'payment_method',

    )

    inlines = [

        OrderItemInline,

    ]
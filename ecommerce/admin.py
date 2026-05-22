from django.contrib import admin

from accounts.admin import admin_site

from .models import (

    Category,
    SubCategory,
    ChildCategory,

    Product,
    ProductImage,

    Shop,

    SmartSharePlan,
    SmartShareIncome,

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
# CHILD CATEGORY ADMIN
# =========================

@admin.register(ChildCategory, site=admin_site)
class ChildCategoryAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'category',
        'subcategory',
        'created_at',

    )

    search_fields = (

        'name',

    )

    list_filter = (

        'category',
        'subcategory',

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
        'child_category',
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
        'child_category',
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
# SMART SHARE PLAN ADMIN
# =========================

@admin.register(SmartSharePlan, site=admin_site)
class SmartSharePlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'plan_type',

        'level_1_income',
        'level_2_income',
        'level_3_income',
        'level_4_income',
        'level_5_income',

        'coin_free',
        'coin_paid',

        'shop_coin_free',
        'shop_coin_paid',

        'is_active',

    )

    search_fields = (

        'name',

    )

    list_filter = (

        'plan_type',
        'is_active',

    )


# =========================
# SMART SHARE INCOME ADMIN
# =========================

@admin.register(SmartShareIncome, site=admin_site)
class SmartShareIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'from_user',
        'plan',
        'level',
        'amount',
        'created_at',

    )

    search_fields = (

        'user__email',
        'from_user__email',

    )

    list_filter = (

        'level',
        'plan',

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
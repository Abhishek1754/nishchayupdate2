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

    ShopCashbackPlan,
    ShopPurchase,
    ShopDailyQueue,
    ShopChainIncome,
    ConsumerReferralPlan,
    ConsumerReferralIncome,

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
# SHOP CASHBACK PLAN ADMIN
# =========================

@admin.register(ShopCashbackPlan, site=admin_site)
class ShopCashbackPlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'self_cashback_percentage',
        'chain_cashback_percentage',
        'total_chain_users',
        'is_active',
        'created_at',

    )

    search_fields = (

        'name',

    )

    list_filter = (

        'is_active',

    )


# =========================
# SHOP PURCHASE ADMIN
# =========================

@admin.register(ShopPurchase, site=admin_site)
class ShopPurchaseAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'shop',
        'amount',
        'cashback_amount',
        'purchase_date',
        'created_at',

    )

    search_fields = (

        'user__email',
        'shop__name',

    )

    list_filter = (

        'purchase_date',
        'shop',

    )


# =========================
# SHOP DAILY QUEUE ADMIN
# =========================

@admin.register(ShopDailyQueue, site=admin_site)
class ShopDailyQueueAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'shop',
        'user',
        'queue_position',
        'queue_date',
        'created_at',

    )

    search_fields = (

        'user__email',
        'shop__name',

    )

    list_filter = (

        'queue_date',
        'shop',

    )


# =========================
# SHOP CHAIN INCOME ADMIN
# =========================

@admin.register(ShopChainIncome, site=admin_site)
class ShopChainIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'shop',
        'user',
        'from_user',
        'level',
        'amount',
        'income_date',
        'created_at',

    )

    search_fields = (

        'user__email',
        'from_user__email',
        'shop__name',

    )

    list_filter = (

        'income_date',
        'shop',
        'level',

    )
    
    
    # =========================
# CONSUMER REFERRAL PLAN ADMIN
# =========================

@admin.register(ConsumerReferralPlan, site=admin_site)
class ConsumerReferralPlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'direct_percentage',
        'indirect_percentage',
        'total_levels',
        'is_active',
        'created_at',

    )

    search_fields = (

        'name',

    )

    list_filter = (

        'is_active',

    )


# =========================
# CONSUMER REFERRAL INCOME ADMIN
# =========================

@admin.register(ConsumerReferralIncome, site=admin_site)
class ConsumerReferralIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'from_user',
        'level',
        'purchase_amount',
        'commission_amount',
        'created_at',

    )

    search_fields = (

        'user__email',
        'from_user__email',

    )

    list_filter = (

        'level',

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
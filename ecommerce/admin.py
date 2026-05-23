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
    StoreBoostPlan,
    StoreBoostBusiness,
    StoreBoostIncome,
    RegionalConnectPlan,
    RegionalFranchise,
    RegionalFranchiseShop,
    RegionalConnectIncome,

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
# STORE BOOST PLAN ADMIN
# =========================

@admin.register(StoreBoostPlan, site=admin_site)
class StoreBoostPlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'nishchay_commission_percentage',
        'direct_income_percentage',
        'indirect_income_percentage',
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
# STORE BOOST BUSINESS ADMIN
# =========================

@admin.register(StoreBoostBusiness, site=admin_site)
class StoreBoostBusinessAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'shop',
        'month',
        'year',
        'total_business',
        'nishchay_profit',
        'created_at',

    )

    search_fields = (

        'user__email',
        'shop__name',

    )

    list_filter = (

        'month',
        'year',
        'shop',

    )


# =========================
# STORE BOOST INCOME ADMIN
# =========================

@admin.register(StoreBoostIncome, site=admin_site)
class StoreBoostIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'from_user',
        'level',
        'total_business',
        'nishchay_profit',
        'commission_percentage',
        'commission_amount',
        'month',
        'year',
        'created_at',

    )

    search_fields = (

        'user__email',
        'from_user__email',

    )

    list_filter = (

        'level',
        'month',
        'year',

    )
    
    
    # =========================
# REGIONAL CONNECT PLAN ADMIN
# =========================

@admin.register(RegionalConnectPlan, site=admin_site)
class RegionalConnectPlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'minimum_team_size',
        'team_level_depth',
        'nishchay_commission_percentage',
        'franchise_income_percentage',
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
# REGIONAL FRANCHISE ADMIN
# =========================

@admin.register(RegionalFranchise, site=admin_site)
class RegionalFranchiseAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'state',
        'district',
        'city',
        'pincode',
        'total_team_size',
        'total_shops',
        'status',
        'is_active',
        'created_at',

    )

    search_fields = (

        'user__email',
        'state',
        'district',
        'city',

    )

    list_filter = (

        'status',
        'state',
        'is_active',

    )


# =========================
# REGIONAL FRANCHISE SHOP ADMIN
# =========================

@admin.register(RegionalFranchiseShop, site=admin_site)
class RegionalFranchiseShopAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'franchise',
        'shop',
        'created_at',

    )

    search_fields = (

        'franchise__user__email',
        'shop__name',

    )


# =========================
# REGIONAL CONNECT INCOME ADMIN
# =========================

@admin.register(RegionalConnectIncome, site=admin_site)
class RegionalConnectIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'franchise',
        'user',
        'total_shop_profit',
        'nishchay_profit',
        'franchise_percentage',
        'franchise_income',
        'month',
        'year',
        'created_at',

    )

    search_fields = (

        'user__email',

    )

    list_filter = (

        'month',
        'year',

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
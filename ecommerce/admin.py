from django.contrib import admin

from accounts.admin import admin_site

from django.utils.html import format_html

from .models import (

    Category,
    SubCategory,
    ChildCategory,

    Product,
    ProductImage,

    Shop,

   

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
    MasterConnectPlan,
    MasterConnect,
    MasterConnectShop,
    MasterConnectIncome,
    MonthlyCouponCampaign,
    MonthlyCouponEligibility,
    MonthlyCouponUser,
    Banner,

    Cart,

    Order,
    OrderItem,
    Address,

)


# =========================
# PRODUCT IMAGE INLINE
# =========================

class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 0

    max_num = 4


# =========================
# CATEGORY ADMIN
# =========================

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (

    "id",

    "name",

    "display_order",

    "is_active",

    "created_at",

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

    "id",

    "name",

    "category",

    "display_order",

    "is_active",

    "created_at",

)

    search_fields = (

        'name',

    )

    list_filter = (

    "category",

    "is_active",

)
    
    ordering = (

    "display_order",

)


# =========================
# CHILD CATEGORY ADMIN
# =========================

@admin.register(ChildCategory, site=admin_site)
class ChildCategoryAdmin(admin.ModelAdmin):

    list_display = (

    "id",

    "name",

    "category",

    "subcategory",

    "display_order",

    "is_active",

    "created_at",

)

    search_fields = (

        'name',

    )
    
    list_filter = (

        "is_active",

    )

    ordering = (

        "display_order",

    )

    list_filter = (

    "category",

    "subcategory",

    "is_active",

)
    
    ordering = (

    "display_order",

)


# =========================
# PRODUCT ADMIN
# =========================

@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):

    list_display = (

    "id",

    "preview",

    "name",

    "category",

    "subcategory",

    "child_category",

    "price",

    "quantity",

    "is_featured",

    "is_flash_deal",

    "is_trending",

    "is_best_seller",

    "is_active",

)

    search_fields = (

    "name",

    "sku",

    "brand",

)
    
    ordering = (

    "display_order",

    "-id",

)
    

    list_filter = (

    "category",

    "subcategory",

    "child_category",

    "is_featured",

    "is_flash_deal",

    "is_trending",

    "is_best_seller",

    "is_active",

)

    inlines = [

        ProductImageInline,

    ]
    
    def preview(self, obj):

        image = obj.images.first()

        if image:

            return format_html(
                '<img src="{}" width="55" height="55" style="border-radius:10px;">',
                image.image.url
            )

        return "-"

    preview.short_description = "Image"
    
    
    



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
# MASTER CONNECT PLAN ADMIN
# =========================

@admin.register(MasterConnectPlan, site=admin_site)
class MasterConnectPlanAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'minimum_regional_connects',
        'minimum_team_size',
        'team_level_depth',
        'nishchay_commission_percentage',
        'master_income_percentage',
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
# MASTER CONNECT ADMIN
# =========================

@admin.register(MasterConnect, site=admin_site)
class MasterConnectAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'total_team_size',
        'total_regional_connects',
        'total_shops',
        'status',
        'is_active',
        'created_at',

    )

    search_fields = (

        'user__email',

    )

    list_filter = (

        'status',
        'is_active',

    )


# =========================
# MASTER CONNECT SHOP ADMIN
# =========================

@admin.register(MasterConnectShop, site=admin_site)
class MasterConnectShopAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'master_connect',
        'shop',
        'created_at',

    )

    search_fields = (

        'master_connect__user__email',
        'shop__name',

    )


# =========================
# MASTER CONNECT INCOME ADMIN
# =========================

@admin.register(MasterConnectIncome, site=admin_site)
class MasterConnectIncomeAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'master_connect',
        'user',
        'total_shop_business',
        'nishchay_profit',
        'master_percentage',
        'master_income',
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
# MONTHLY COUPON ELIGIBILITY INLINE
# =========================

class MonthlyCouponEligibilityInline(admin.TabularInline):

    model = MonthlyCouponEligibility

    extra = 1


# =========================
# MONTHLY COUPON CAMPAIGN ADMIN
# =========================

@admin.register(MonthlyCouponCampaign, site=admin_site)
class MonthlyCouponCampaignAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'coupon_code',
        'discount_percentage',
        'maximum_discount_amount',
        'valid_from',
        'valid_to',
        'total_usage_limit',
        'per_user_limit',
        'is_active',
        'created_at',

    )

    search_fields = (

        'name',
        'coupon_code',

    )

    list_filter = (

        'is_active',
        'valid_from',
        'valid_to',

    )

    inlines = [

        MonthlyCouponEligibilityInline,

    ]


# =========================
# MONTHLY COUPON ELIGIBILITY ADMIN
# =========================

@admin.register(MonthlyCouponEligibility, site=admin_site)
class MonthlyCouponEligibilityAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'campaign',
        'condition_type',
        'minimum_value',
        'created_at',

    )

    search_fields = (

        'campaign__name',

    )

    list_filter = (

        'condition_type',

    )


# =========================
# MONTHLY COUPON USER ADMIN
# =========================

@admin.register(MonthlyCouponUser, site=admin_site)
class MonthlyCouponUserAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'campaign',
        'user',
        'status',
        'month',
        'year',
        'used_at',
        'created_at',

    )

    search_fields = (

        'user__email',
        'campaign__name',

    )

    list_filter = (

        'status',
        'month',
        'year',

    )
    
# =========================
# HOME BANNER ADMIN
# =========================

@admin.register(Banner, site=admin_site)
class BannerAdmin(admin.ModelAdmin):

    list_display = (

        "id",
        "title",
        "display_order",
        "is_active",
        "created_at",

    )

    list_filter = (

        "is_active",

    )

    search_fields = (

        "title",
        "heading",

    )

    ordering = (

        "display_order",

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
    
    # =====================================
# CUSTOMER ADDRESS
# =====================================

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (

        "id",
        "user",
        "full_name",
        "mobile_number",
        "city",
        "state",
        "pincode",
        "address_type",
        "is_default",

    )

    list_filter = (

        "state",
        "city",
        "address_type",
        "is_default",

    )

    search_fields = (

        "full_name",
        "mobile_number",
        "city",
        "state",
        "pincode",
        "user__email",
        "user__phone",

    )

    ordering = (

        "-id",

    )
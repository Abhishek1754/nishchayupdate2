from django.contrib import admin
from django.utils import timezone

from accounts.admin import admin_site

from .models import (

    Restaurant,
    FoodCategory,
    FoodItem,
    FoodItemImage,

    DeliveryAddress,

    FoodCart,

    GroupOrder,
    GroupOrderMember,

    FoodOrder,
    FoodOrderItem,

    DeliveryPartner,

    OrderTrackingLog,

)


# =====================================================
# FOOD ITEM IMAGE INLINE
# =====================================================

class FoodItemImageInline(admin.TabularInline):

    model = FoodItemImage

    extra = 1

    max_num = 5


# =====================================================
# FOOD ORDER ITEM INLINE
# =====================================================

class FoodOrderItemInline(admin.TabularInline):

    model = FoodOrderItem

    extra = 0


# =====================================================
# GROUP ORDER MEMBER INLINE
# =====================================================

class GroupOrderMemberInline(admin.TabularInline):

    model = GroupOrderMember

    extra = 0


# =====================================================
# ORDER TRACKING INLINE
# =====================================================

class OrderTrackingLogInline(admin.TabularInline):

    model = OrderTrackingLog

    extra = 0

    readonly_fields = (

        'status',
        'note',
        'latitude',
        'longitude',
        'created_at',

    )


# =====================================================
# RESTAURANT ADMIN
# =====================================================

@admin.register(Restaurant, site=admin_site)
class RestaurantAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'owner',
        'city',
        'state',
        'phone',
        'rating',
        'is_open',
        'is_active',
        'created_at',

    )

    search_fields = (

        'name',
        'owner__email',
        'city',
        'state',

    )

    list_filter = (

        'is_open',
        'is_active',
        'city',
        'state',

    )

    prepopulated_fields = {

        'slug': ('name',)

    }


# =====================================================
# FOOD CATEGORY ADMIN
# =====================================================

@admin.register(FoodCategory, site=admin_site)
class FoodCategoryAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'restaurant',
        'is_active',
        'created_at',

    )

    search_fields = (

        'name',
        'restaurant__name',

    )

    list_filter = (

        'is_active',

    )


# =====================================================
# FOOD ITEM ADMIN
# =====================================================

@admin.register(FoodItem, site=admin_site)
class FoodItemAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'name',
        'restaurant',
        'category',
        'food_type',
        'price',
        'discount_price',
        'stock',
        'is_available',
        'is_featured',
        'created_at',

    )

    search_fields = (

        'name',
        'restaurant__name',

    )

    list_filter = (

        'food_type',
        'is_available',
        'is_featured',

    )

    inlines = [

        FoodItemImageInline,

    ]


# =====================================================
# FOOD ITEM IMAGE ADMIN
# =====================================================

@admin.register(FoodItemImage, site=admin_site)
class FoodItemImageAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'food_item',
        'created_at',

    )

    search_fields = (

        'food_item__name',

    )


# =====================================================
# DELIVERY ADDRESS ADMIN
# =====================================================

@admin.register(DeliveryAddress, site=admin_site)
class DeliveryAddressAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'city',
        'state',
        'pincode',
        'is_default',
        'created_at',

    )

    search_fields = (

        'user__email',
        'city',
        'state',

    )

    list_filter = (

        'is_default',
        'city',
        'state',

    )


# =====================================================
# FOOD CART ADMIN
# =====================================================

@admin.register(FoodCart, site=admin_site)
class FoodCartAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'food_item',
        'quantity',
        'created_at',

    )

    search_fields = (

        'user__email',
        'food_item__name',

    )


# =====================================================
# GROUP ORDER ADMIN
# =====================================================

@admin.register(GroupOrder, site=admin_site)
class GroupOrderAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'title',
        'group_code',
        'restaurant',
        'created_by',
        'total_members',
        'total_amount',
        'cashback_percentage',
        'status',
        'expires_at',
        'created_at',

    )

    search_fields = (

        'title',
        'group_code',
        'created_by__email',

    )

    list_filter = (

        'status',

    )

    inlines = [

        GroupOrderMemberInline,

    ]


# =====================================================
# GROUP ORDER MEMBER ADMIN
# =====================================================

@admin.register(GroupOrderMember, site=admin_site)
class GroupOrderMemberAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'group_order',
        'user',
        'total_amount',
        'joined_at',

    )

    search_fields = (

        'user__email',
        'group_order__title',

    )


# =====================================================
# FOOD ORDER ADMIN
# =====================================================

@admin.register(FoodOrder, site=admin_site)
class FoodOrderAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'order_number',
        'user',
        'restaurant',
        'delivery_partner',
        'total_amount',
        'payment_method',
        'status',
        'estimated_delivery_time',
        'created_at',

    )

    search_fields = (

        'order_number',
        'user__email',
        'restaurant__name',

    )

    list_filter = (

        'status',
        'payment_method',

    )

    readonly_fields = (

        'accepted_at',
        'picked_at',
        'delivered_at',

    )

    inlines = [

        FoodOrderItemInline,

        OrderTrackingLogInline,

    ]

    actions = [

        'mark_preparing',

        'mark_ready',

        'mark_picked',

        'mark_nearby',

        'mark_delivered',

    ]

    # =====================================================
    # MARK PREPARING
    # =====================================================

    def mark_preparing(

        self,
        request,
        queryset

    ):

        queryset.update(
            status='preparing'
        )

    mark_preparing.short_description = (

        "Mark selected orders as PREPARING"

    )

    # =====================================================
    # MARK READY
    # =====================================================

    def mark_ready(

        self,
        request,
        queryset

    ):

        queryset.update(
            status='ready'
        )

    mark_ready.short_description = (

        "Mark selected orders as READY"

    )

    # =====================================================
    # MARK PICKED
    # =====================================================

    def mark_picked(

        self,
        request,
        queryset

    ):

        queryset.update(

            status='picked',

            picked_at=timezone.now()

        )

    mark_picked.short_description = (

        "Mark selected orders as PICKED"

    )

    # =====================================================
    # MARK NEARBY
    # =====================================================

    def mark_nearby(

        self,
        request,
        queryset

    ):

        queryset.update(
            status='nearby'
        )

    mark_nearby.short_description = (

        "Mark selected orders as NEARBY"

    )

    # =====================================================
    # MARK DELIVERED
    # =====================================================

    def mark_delivered(

        self,
        request,
        queryset

    ):

        queryset.update(

            status='delivered',

            delivered_at=timezone.now()

        )

    mark_delivered.short_description = (

        "Mark selected orders as DELIVERED"

    )


# =====================================================
# FOOD ORDER ITEM ADMIN
# =====================================================

@admin.register(FoodOrderItem, site=admin_site)
class FoodOrderItemAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'order',
        'food_item',
        'quantity',
        'price',
        'total_price',

    )

    search_fields = (

        'order__order_number',
        'food_item__name',

    )


# =====================================================
# DELIVERY PARTNER ADMIN
# =====================================================

@admin.register(DeliveryPartner, site=admin_site)
class DeliveryPartnerAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'vehicle_number',
        'current_order',
        'is_available',
        'total_deliveries',
        'total_earnings',
        'status',
        'is_verified',
        'created_at',

    )

    search_fields = (

        'user__email',
        'vehicle_number',

    )

    list_filter = (

        'status',
        'is_verified',
        'is_available',

    )

    actions = [

        'mark_online',

        'mark_offline',

    ]

    # =====================================================
    # MARK ONLINE
    # =====================================================

    def mark_online(

        self,
        request,
        queryset

    ):

        queryset.update(
            status='online'
        )

    mark_online.short_description = (

        "Mark selected riders ONLINE"

    )

    # =====================================================
    # MARK OFFLINE
    # =====================================================

    def mark_offline(

        self,
        request,
        queryset

    ):

        queryset.update(
            status='offline'
        )

    mark_offline.short_description = (

        "Mark selected riders OFFLINE"

    )


# =====================================================
# ORDER TRACKING LOG ADMIN
# =====================================================

@admin.register(OrderTrackingLog, site=admin_site)
class OrderTrackingLogAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'order',
        'status',
        'created_at',

    )

    search_fields = (

        'order__order_number',
        'status',

    )

    list_filter = (

        'status',

    )
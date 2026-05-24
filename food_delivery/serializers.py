from rest_framework import serializers

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
# FOOD ITEM IMAGE SERIALIZER
# =====================================================

class FoodItemImageSerializer(

    serializers.ModelSerializer

):

    class Meta:

        model = FoodItemImage

        fields = '__all__'


# =====================================================
# FOOD CATEGORY SERIALIZER
# =====================================================

class FoodCategorySerializer(

    serializers.ModelSerializer

):

    class Meta:

        model = FoodCategory

        fields = '__all__'


# =====================================================
# FOOD ITEM SERIALIZER
# =====================================================

class FoodItemSerializer(

    serializers.ModelSerializer

):

    images = FoodItemImageSerializer(

        many=True,
        read_only=True

    )

    category_name = serializers.CharField(

        source='category.name',
        read_only=True

    )

    restaurant_name = serializers.CharField(

        source='restaurant.name',
        read_only=True

    )

    class Meta:

        model = FoodItem

        fields = '__all__'


# =====================================================
# RESTAURANT SERIALIZER
# =====================================================

class RestaurantSerializer(

    serializers.ModelSerializer

):

    categories = FoodCategorySerializer(

        many=True,
        read_only=True

    )

    class Meta:

        model = Restaurant

        fields = '__all__'


# =====================================================
# DELIVERY ADDRESS SERIALIZER
# =====================================================

class DeliveryAddressSerializer(

    serializers.ModelSerializer

):

    class Meta:

        model = DeliveryAddress

        fields = '__all__'


# =====================================================
# FOOD CART SERIALIZER
# =====================================================

class FoodCartSerializer(

    serializers.ModelSerializer

):

    food_item = FoodItemSerializer(
        read_only=True
    )

    food_item_id = serializers.IntegerField(
        write_only=True
    )

    class Meta:

        model = FoodCart

        fields = (

            'id',
            'user',
            'food_item',
            'food_item_id',
            'quantity',
            'created_at',

        )

        read_only_fields = (

            'user',

        )


# =====================================================
# GROUP ORDER MEMBER SERIALIZER
# =====================================================

class GroupOrderMemberSerializer(

    serializers.ModelSerializer

):

    user_email = serializers.CharField(

        source='user.email',
        read_only=True

    )

    class Meta:

        model = GroupOrderMember

        fields = '__all__'


# =====================================================
# GROUP ORDER SERIALIZER
# =====================================================

class GroupOrderSerializer(

    serializers.ModelSerializer

):

    members = GroupOrderMemberSerializer(

        many=True,
        read_only=True

    )

    restaurant_name = serializers.CharField(

        source='restaurant.name',
        read_only=True

    )

    created_by_email = serializers.CharField(

        source='created_by.email',
        read_only=True

    )

    class Meta:

        model = GroupOrder

        fields = '__all__'


# =====================================================
# FOOD ORDER ITEM SERIALIZER
# =====================================================

class FoodOrderItemSerializer(

    serializers.ModelSerializer

):

    food_item_name = serializers.CharField(

        source='food_item.name',
        read_only=True

    )

    class Meta:

        model = FoodOrderItem

        fields = '__all__'


# =====================================================
# ORDER TRACKING LOG SERIALIZER
# =====================================================

class OrderTrackingLogSerializer(

    serializers.ModelSerializer

):

    class Meta:

        model = OrderTrackingLog

        fields = '__all__'


# =====================================================
# DELIVERY PARTNER SERIALIZER
# =====================================================

class DeliveryPartnerSerializer(

    serializers.ModelSerializer

):

    user_email = serializers.CharField(

        source='user.email',
        read_only=True

    )

    current_order_number = serializers.CharField(

        source='current_order.order_number',
        read_only=True

    )

    class Meta:

        model = DeliveryPartner

        fields = '__all__'


# =====================================================
# FOOD ORDER SERIALIZER
# =====================================================

class FoodOrderSerializer(

    serializers.ModelSerializer

):

    items = FoodOrderItemSerializer(

        many=True,
        read_only=True

    )

    tracking_logs = OrderTrackingLogSerializer(

        many=True,
        read_only=True

    )

    restaurant_name = serializers.CharField(

        source='restaurant.name',
        read_only=True

    )

    user_email = serializers.CharField(

        source='user.email',
        read_only=True

    )

    delivery_partner = DeliveryPartnerSerializer(
        read_only=True
    )

    delivery_partner_id = serializers.IntegerField(
        write_only=True,
        required=False
    )

    class Meta:

        model = FoodOrder

        fields = '__all__'


# =====================================================
# LIVE TRACKING SERIALIZER
# =====================================================

class LiveTrackingSerializer(

    serializers.ModelSerializer

):

    delivery_partner_name = serializers.CharField(

        source='delivery_partner.user.email',
        read_only=True

    )

    class Meta:

        model = FoodOrder

        fields = (

            'id',

            'order_number',

            'status',

            'estimated_delivery_time',

            'live_latitude',

            'live_longitude',

            'delivery_partner_name',

        )
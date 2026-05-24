from django.db import models

from accounts.models import User


# =====================================================
# RESTAURANT
# =====================================================

class Restaurant(models.Model):

    owner = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name='restaurants'

    )

    name = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    logo = models.ImageField(
        upload_to='restaurant/logo/',
        blank=True,
        null=True
    )

    banner = models.ImageField(
        upload_to='restaurant/banner/',
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    gst_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    opening_time = models.TimeField()

    closing_time = models.TimeField()

    delivery_radius_km = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5
    )

    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    total_reviews = models.IntegerField(
        default=0
    )

    is_open = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.name


# =====================================================
# FOOD CATEGORY
# =====================================================

class FoodCategory(models.Model):

    restaurant = models.ForeignKey(

        Restaurant,

        on_delete=models.CASCADE,

        related_name='categories'

    )

    name = models.CharField(
        max_length=255
    )

    image = models.ImageField(
        upload_to='food/category/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =====================================================
# FOOD ITEM
# =====================================================

class FoodItem(models.Model):

    FOOD_TYPES = (

        ('veg', 'Veg'),
        ('nonveg', 'Non Veg'),
        ('egg', 'Egg'),

    )

    restaurant = models.ForeignKey(

        Restaurant,

        on_delete=models.CASCADE,

        related_name='food_items'

    )

    category = models.ForeignKey(

        FoodCategory,

        on_delete=models.CASCADE,

        related_name='food_items'

    )

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='food/items/',
        blank=True,
        null=True
    )

    food_type = models.CharField(
        max_length=20,
        choices=FOOD_TYPES,
        default='veg'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    preparation_time = models.IntegerField(
        default=15
    )

    calories = models.IntegerField(
        blank=True,
        null=True
    )

    stock = models.IntegerField(
        default=100
    )

    is_available = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.name


# =====================================================
# FOOD ITEM IMAGE
# =====================================================

class FoodItemImage(models.Model):

    food_item = models.ForeignKey(

        FoodItem,

        on_delete=models.CASCADE,

        related_name='images'

    )

    image = models.ImageField(
        upload_to='food/item_gallery/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.food_item.name


# =====================================================
# DELIVERY ADDRESS
# =====================================================

class DeliveryAddress(models.Model):

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name='delivery_addresses'

    )

    full_name = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    landmark = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    is_default = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.city}"


# =====================================================
# FOOD CART
# =====================================================

class FoodCart(models.Model):

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    food_item = models.ForeignKey(

        FoodItem,

        on_delete=models.CASCADE

    )

    quantity = models.IntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.food_item.name}"


# =====================================================
# GROUP ORDER
# =====================================================

class GroupOrder(models.Model):

    STATUS_CHOICES = (

        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),

    )

    restaurant = models.ForeignKey(

        Restaurant,

        on_delete=models.CASCADE

    )

    created_by = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name='created_group_orders'

    )

    group_code = models.CharField(
        max_length=20,
        unique=True
    )

    title = models.CharField(
        max_length=255
    )

    total_members = models.IntegerField(
        default=1
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    expires_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title


# =====================================================
# GROUP ORDER MEMBER
# =====================================================

class GroupOrderMember(models.Model):

    group_order = models.ForeignKey(

        GroupOrder,

        on_delete=models.CASCADE,

        related_name='members'

    )

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email}"


# =====================================================
# FOOD ORDER
# =====================================================

class FoodOrder(models.Model):

    PAYMENT_METHODS = (

        ('cod', 'Cash On Delivery'),
        ('online', 'Online'),
        ('wallet', 'Wallet'),

    )

    STATUS_CHOICES = (

        ('pending', 'Pending'),

        ('accepted', 'Accepted'),

        ('preparing', 'Preparing'),

        ('ready', 'Ready'),

        ('picked', 'Picked'),

        ('nearby', 'Nearby'),

        ('delivered', 'Delivered'),

        ('cancelled', 'Cancelled'),

    )

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    restaurant = models.ForeignKey(

        Restaurant,

        on_delete=models.CASCADE

    )

    delivery_address = models.ForeignKey(

        DeliveryAddress,

        on_delete=models.SET_NULL,

        null=True

    )

    group_order = models.ForeignKey(

        GroupOrder,

        on_delete=models.SET_NULL,

        null=True,
        blank=True

    )

    order_number = models.CharField(
        max_length=50,
        unique=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    delivery_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    cashback_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    estimated_delivery_time = models.DateTimeField(
        blank=True,
        null=True
    )

    accepted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    picked_at = models.DateTimeField(
        blank=True,
        null=True
    )

    delivered_at = models.DateTimeField(
        blank=True,
        null=True
    )

    delivery_partner = models.ForeignKey(

        'DeliveryPartner',

        on_delete=models.SET_NULL,

        blank=True,
        null=True,

        related_name='orders'

    )

    live_latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    live_longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.order_number


# =====================================================
# FOOD ORDER ITEM
# =====================================================

class FoodOrderItem(models.Model):

    order = models.ForeignKey(

        FoodOrder,

        on_delete=models.CASCADE,

        related_name='items'

    )

    food_item = models.ForeignKey(

        FoodItem,

        on_delete=models.CASCADE

    )

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):

        return self.food_item.name


# =====================================================
# DELIVERY PARTNER
# =====================================================

class DeliveryPartner(models.Model):

    STATUS_CHOICES = (

        ('online', 'Online'),
        ('offline', 'Offline'),

    )

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE

    )

    vehicle_number = models.CharField(
        max_length=50
    )

    driving_license = models.CharField(
        max_length=100
    )

    aadhaar_number = models.CharField(
        max_length=20
    )

    current_latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    current_longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    total_deliveries = models.IntegerField(
        default=0
    )

    total_earnings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='offline'
    )

    is_available = models.BooleanField(
        default=True
    )

    current_order = models.ForeignKey(

        FoodOrder,

        on_delete=models.SET_NULL,

        blank=True,
        null=True,

        related_name='active_delivery_partner'

    )

    last_active_at = models.DateTimeField(
        auto_now=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.email


# =====================================================
# ORDER TRACKING LOG
# =====================================================

class OrderTrackingLog(models.Model):

    order = models.ForeignKey(

        FoodOrder,

        on_delete=models.CASCADE,

        related_name='tracking_logs'

    )

    status = models.CharField(
        max_length=50
    )

    note = models.TextField(
        blank=True,
        null=True
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.order.order_number} - {self.status}"
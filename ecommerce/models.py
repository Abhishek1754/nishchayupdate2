from django.db import models

from accounts.models import User

# 🔥 REAL-TIME IMPORTS
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# =========================
# CATEGORY
# =========================

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================
# SUB CATEGORY
# =========================

class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    name = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.category.name} - {self.name}"


# =========================
# CHILD CATEGORY
# =========================

class ChildCategory(models.Model):

    category = models.ForeignKey(

        Category,

        on_delete=models.CASCADE,

        related_name='child_categories'

    )

    subcategory = models.ForeignKey(

        SubCategory,

        on_delete=models.CASCADE,

        related_name='child_categories'

    )

    name = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.category.name} - {self.subcategory.name} - {self.name}"


# =========================
# PRODUCT
# =========================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    child_category = models.ForeignKey(

        ChildCategory,

        on_delete=models.SET_NULL,

        null=True,

        blank=True

    )

    name = models.CharField(
        max_length=200
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    quantity = models.IntegerField()

    cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================
# PRODUCT IMAGES
# =========================

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='products/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.product.name

    def save(self, *args, **kwargs):

        if self.product.images.count() >= 4:

            raise ValueError(
                "Maximum 4 images allowed"
            )

        super().save(*args, **kwargs)


# =========================
# SHOP
# =========================

class Shop(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=200
    )

    gst_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    pan_number = models.CharField(
        max_length=50
    )

    referral_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_paid = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================
# SMART SHARE PLAN
# =========================

class SmartSharePlan(models.Model):

    PLAN_TYPES = (

        ('free', 'Free'),

        ('paid', 'Paid'),

    )

    name = models.CharField(
        max_length=100
    )

    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPES
    )

    total_levels = models.IntegerField(
        default=5
    )

    level_1_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    level_2_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    level_3_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    level_4_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    level_5_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    coin_free = models.IntegerField(
        default=0
    )

    coin_paid = models.IntegerField(
        default=0
    )

    shop_coin_free = models.IntegerField(
        default=0
    )

    shop_coin_paid = models.IntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.name} ({self.plan_type})"


# =========================
# SMART SHARE INCOME
# =========================

class SmartShareIncome(models.Model):

    plan = models.ForeignKey(
        SmartSharePlan,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='smartshare_user'
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='smartshare_from_user'
    )

    level = models.IntegerField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - Level {self.level}"


# =========================
# SHOP CASHBACK PLAN
# =========================

class ShopCashbackPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    self_cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5
    )

    chain_cashback_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1
    )

    total_chain_users = models.IntegerField(
        default=5
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name
    
class Meta:

  verbose_name = "Cashback 360"

verbose_name_plural = "Cashback 360"


# =========================
# SHOP PURCHASE
# =========================

class ShopPurchase(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    cashback_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    purchase_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.shop.name}"


# =========================
# SHOP DAILY QUEUE
# =========================

class ShopDailyQueue(models.Model):

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    purchase = models.ForeignKey(
        ShopPurchase,
        on_delete=models.CASCADE
    )

    queue_position = models.IntegerField()

    queue_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['queue_position']

    def __str__(self):

        return f"{self.shop.name} - {self.user.email}"


# =========================
# SHOP CHAIN INCOME
# =========================

class ShopChainIncome(models.Model):

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    purchase = models.ForeignKey(
        ShopPurchase,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_chain_user'
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_chain_from_user'
    )

    level = models.IntegerField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    income_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - Level {self.level}"
    
    
    # =========================
# CONSUMER REFERRAL PLAN
# =========================

class ConsumerReferralPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    direct_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=4
    )

    indirect_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1
    )

    total_levels = models.IntegerField(
        default=5
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================
# CONSUMER REFERRAL INCOME
# =========================

class ConsumerReferralIncome(models.Model):

    plan = models.ForeignKey(
        ConsumerReferralPlan,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='consumer_referral_user'
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='consumer_referral_from_user'
    )

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    level = models.IntegerField()

    purchase_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    commission_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - Level {self.level}"


# =========================
# CART
# =========================

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.product.name}"


# =========================
# ORDER SYSTEM
# =========================

class Order(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),

    )

    PAYMENT_CHOICES = (

        ('wallet', 'Wallet'),
        ('online', 'Online'),
        ('cod', 'Cash On Delivery'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    cashback_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='wallet'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Order {self.id}"

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:

            channel_layer = get_channel_layer()

            async_to_sync(
                channel_layer.group_send
            )(

                "dashboard",

                {

                    "type": "send_dashboard_update",

                    "data": {

                        "type": "new_order",

                        "order_id": self.id,

                        "user": self.user.email,

                        "amount": str(self.total_amount)

                    }

                }

            )


# =========================
# ORDER ITEM
# =========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):

        return f"{self.product.name} ({self.quantity})"
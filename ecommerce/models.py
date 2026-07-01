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

    SUBSCRIPTION_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
    )

    KYC_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # =========================
    # SHOP BASIC DETAILS
    # =========================

    shop_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    name = models.CharField(
        max_length=200
    )

    owner_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    shop_category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    full_address = models.TextField(
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    latitude = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    longitude = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # =========================
    # CONTACT DETAILS
    # =========================

    shop_contact = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    owner_contact = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    owner_email = models.EmailField(
        blank=True,
        null=True
    )

    # =========================
    # GST / PAN
    # =========================

    gst_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    pan_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    business_pan = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # =========================
    # BANK DETAILS
    # =========================

    bank_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    account_holder = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    account_number = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )

    ifsc_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # =========================
    # DOCUMENTS
    # =========================

    aadhaar_front = models.ImageField(
        upload_to="shops/aadhaar/",
        blank=True,
        null=True
    )

    aadhaar_back = models.ImageField(
        upload_to="shops/aadhaar/",
        blank=True,
        null=True
    )

    pan_card = models.ImageField(
        upload_to="shops/pan/",
        blank=True,
        null=True
    )

    business_pan_file = models.ImageField(
        upload_to="shops/business_pan/",
        blank=True,
        null=True
    )

    shop_photo = models.ImageField(
        upload_to="shops/photos/",
        blank=True,
        null=True
    )

    # =========================
    # REGISTRATION
    # =========================

    referral_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    subscription_type = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default="free"
    )

    subscription_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    subscription_expiry = models.DateField(
        blank=True,
        null=True
    )

    is_paid = models.BooleanField(
        default=False
    )

    is_verified = models.BooleanField(
        default=False
    )

    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =========================
    # AUTO SHOP ID
    # =========================

    def save(self, *args, **kwargs):

        if not self.shop_id:

            last_shop = Shop.objects.order_by('-id').first()

            if last_shop:
                next_id = last_shop.id + 1
            else:
                next_id = 1

            self.shop_id = f"NSHSHOP{next_id:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
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
# STORE BOOST PLAN
# =========================

class StoreBoostPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    nishchay_commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=3
    )

    direct_income_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=3
    )

    indirect_income_percentage = models.DecimalField(
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
# STORE BOOST BUSINESS
# =========================

class StoreBoostBusiness(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='store_boost_business_user'
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    month = models.IntegerField()

    year = models.IntegerField()

    total_business = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    nishchay_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.shop.name}"


# =========================
# STORE BOOST INCOME
# =========================

class StoreBoostIncome(models.Model):

    plan = models.ForeignKey(
        StoreBoostPlan,
        on_delete=models.CASCADE
    )

    business = models.ForeignKey(
        StoreBoostBusiness,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='store_boost_user'
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='store_boost_from_user'
    )

    level = models.IntegerField()

    total_business = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    nishchay_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    commission_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    month = models.IntegerField()

    year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - Level {self.level}"
    
    
    # =========================
# REGIONAL CONNECT PLAN
# =========================

class RegionalConnectPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    minimum_team_size = models.IntegerField(
        default=2000
    )

    team_level_depth = models.IntegerField(
        default=10
    )

    nishchay_commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5
    )

    franchise_income_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=2
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
# REGIONAL FRANCHISE
# =========================

class RegionalFranchise(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    state = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    pincode = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    total_team_size = models.IntegerField(
        default=0
    )

    total_shops = models.IntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.state}"


# =========================
# REGIONAL FRANCHISE SHOP
# =========================

class RegionalFranchiseShop(models.Model):

    franchise = models.ForeignKey(
        RegionalFranchise,
        on_delete=models.CASCADE
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.franchise.user.email} - {self.shop.name}"


# =========================
# REGIONAL CONNECT INCOME
# =========================

class RegionalConnectIncome(models.Model):

    franchise = models.ForeignKey(
        RegionalFranchise,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_shop_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    nishchay_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    franchise_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    franchise_income = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    month = models.IntegerField()

    year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.month}/{self.year}"
    
    
    # =========================
# MASTER CONNECT PLAN
# =========================

class MasterConnectPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    minimum_regional_connects = models.IntegerField(
        default=5
    )

    minimum_team_size = models.IntegerField(
        default=200000
    )

    team_level_depth = models.IntegerField(
        default=10
    )

    nishchay_commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=2.5
    )

    master_income_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.30
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
# MASTER CONNECT
# =========================

class MasterConnect(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_team_size = models.IntegerField(
        default=0
    )

    total_regional_connects = models.IntegerField(
        default=0
    )

    total_shops = models.IntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.email


# =========================
# MASTER CONNECT SHOP
# =========================

class MasterConnectShop(models.Model):

    master_connect = models.ForeignKey(
        MasterConnect,
        on_delete=models.CASCADE
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.master_connect.user.email} - {self.shop.name}"


# =========================
# MASTER CONNECT INCOME
# =========================

class MasterConnectIncome(models.Model):

    master_connect = models.ForeignKey(
        MasterConnect,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_shop_business = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    nishchay_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    master_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    master_income = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    month = models.IntegerField()

    year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.month}/{self.year}"
    
    # =========================
# MONTHLY COUPON CAMPAIGN
# =========================

class MonthlyCouponCampaign(models.Model):

    name = models.CharField(
        max_length=200
    )

    coupon_code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    maximum_discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    valid_from = models.DateField()

    valid_to = models.DateField()

    total_usage_limit = models.IntegerField(
        default=1000
    )

    per_user_limit = models.IntegerField(
        default=1
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
# MONTHLY COUPON ELIGIBILITY
# =========================

class MonthlyCouponEligibility(models.Model):

    CONDITION_TYPES = (

        ('purchase_amount', 'Purchase Amount'),

        ('order_count', 'Order Count'),

        ('shop_purchase_count', 'Shop Purchase Count'),

        ('wallet_balance', 'Wallet Balance'),

        ('roi_investment', 'ROI Investment'),

        ('regional_connect', 'Regional Connect'),

        ('master_connect', 'Master Connect'),

        ('team_size', 'Team Size'),

    )

    campaign = models.ForeignKey(
        MonthlyCouponCampaign,
        on_delete=models.CASCADE,
        related_name='eligibilities'
    )

    condition_type = models.CharField(
        max_length=50,
        choices=CONDITION_TYPES
    )

    minimum_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.campaign.name} - {self.condition_type}"


# =========================
# MONTHLY COUPON USER
# =========================

class MonthlyCouponUser(models.Model):

    STATUS_CHOICES = (

        ('eligible', 'Eligible'),

        ('used', 'Used'),

        ('expired', 'Expired'),

    )

    campaign = models.ForeignKey(
        MonthlyCouponCampaign,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='eligible'
    )

    used_at = models.DateTimeField(
        blank=True,
        null=True
    )

    month = models.IntegerField()

    year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (

            'campaign',
            'user',
            'month',
            'year'

        )

    def __str__(self):

        return f"{self.user.email} - {self.campaign.name}"



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
    payment_status = models.CharField(
    max_length=20,
    default="pending"
)

cashfree_order_id = models.CharField(
    max_length=100,
    blank=True,
    null=True
)

cashfree_payment_id = models.CharField(
    max_length=100,
    blank=True,
    null=True
)

payment_completed_at = models.DateTimeField(
    blank=True,
    null=True
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
    
    # =========================
# CUSTOMER ADDRESS
# =========================

class Address(models.Model):

    ADDRESS_TYPES = (

        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    full_name = models.CharField(
        max_length=200
    )

    mobile_number = models.CharField(
        max_length=15
    )

    alternate_mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    house_no = models.CharField(
        max_length=255
    )

    area = models.CharField(
        max_length=255
    )

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

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default='home'
    )

    is_default = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.full_name} ({self.address_type})"
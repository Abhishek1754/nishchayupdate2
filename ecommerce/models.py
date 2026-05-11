from django.db import models
from accounts.models import User

# 🔥 REAL-TIME IMPORTS
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# =========================
# ORDER SYSTEM (REAL-TIME ENABLED)
# =========================

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

    # 🚀 REAL-TIME TRIGGER (ENTERPRISE FEATURE)
    def save(self, *args, **kwargs):
        is_new = self.pk is None   # ✅ detect new order

        super().save(*args, **kwargs)

        # 🔔 ONLY TRIGGER ON NEW ORDER
        if is_new:
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                "dashboard",
                {
                    "type": "send_dashboard_update",
                    "data": {
                        "type": "new_order",
                        "order_id": self.id,
                        "user": self.user.email,
                        "amount": self.total_amount
                    }
                }
            )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
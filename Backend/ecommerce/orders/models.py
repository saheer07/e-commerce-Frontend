from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from products.models import Product  # assuming your product app is named 'products'

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('RAZORPAY', 'Razorpay'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Ordered")
    purchased_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.CharField(max_length=100)
    card_details = models.JSONField(null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

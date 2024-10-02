
from django.db import models

from product.models import Product
from profiles.models import UserProfile


class Order(models.Model):

    createdAt = models.DateTimeField(auto_now_add=True, blank=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    DELIVERY_CHOICES = (("Delivery", "Delivery"), ("Express delivery", "Express delivery"))
    deliveryType = models.CharField(max_length=50, choices=DELIVERY_CHOICES, blank=True)

    PAYMENT_CHOICES = (
        ("Online card", "Online card"),
        ("Online from random someone else`s account", "Online from random someone else`s account")
    )
    paymentType = models.CharField(max_length=50, choices=PAYMENT_CHOICES, blank=True)

    totalCost = models.DecimalField(max_digits=10, decimal_places=1)

    STATUS_CHOICES = (("Accepted", "Accepted"), ("Unaccepted", "Unaccepted"))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True)

    city = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    """Модель продуктов в заказе"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products_in_order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=1, max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

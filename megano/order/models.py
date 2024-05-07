from django.db import models

from product.models import Product


class Order(models.Model):
    pay_type = (
        ("Online card", "Online card"),
        ("Online from random someone else`s account", "Online from random someone else`s account")
    )
    del_type = (("Delivery", "Delivery"), ("Express delivery", "Express delivery"))
    status_order = (("Accepted", "Accepted"), ("Unaccepted", "Unaccepted"))

    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    full_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=15, blank=False)
    delivery_type = models.CharField(max_length=50, choices=del_type, blank=False)
    payment_type = models.CharField(max_length=50, choices=pay_type, blank=False)
    totalCost = models.DecimalField(max_digits=10, decimal_places=1)
    status = models.CharField(max_length=50, choices=status_order, blank=False)
    city = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=20, blank=False)
    products = models.ManyToManyField(Product, related_name="order_products")



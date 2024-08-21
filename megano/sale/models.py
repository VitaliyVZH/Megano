from django.db import models

from product.models import Product


class ProductSale(models.Model):
    salePrice = models.DecimalField(max_digits=5, decimal_places=2)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
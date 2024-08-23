from django.db import models

from product.models import Product


class ProductSale(models.Model):
    """Реализация модели/таблицы акционных товаров."""

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    salePrice = models.DecimalField(max_digits=5, decimal_places=2)  # цена товара после скидки
    dateFrom = models.DateField()  # дата начала акции/скидки на товар
    dateTo = models.DateField()  # дата окончания акции/скидки на товар
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

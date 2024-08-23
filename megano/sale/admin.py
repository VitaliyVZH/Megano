from django.contrib import admin

from sale.models import ProductSale


@admin.register(ProductSale)
class ProductSaleAdmin(admin.ModelAdmin):
    """Реализация в административной панели раздела с товарами по акции."""

    list_display = 'salePrice', 'dateFrom', 'dateTo', 'product',

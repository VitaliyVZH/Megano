from rest_framework import serializers

from product.models import ProductImage
from sale.models import ProductSale


class ProductSaleSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров со скидками."""

    id = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    salePrice = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductSale
        fields = "id", "price", "salePrice", "title", "dateFrom", "dateTo", "images"

    def get_id(self, obj: ProductSale) -> str:
        return f"{obj.product.pk}"

    def get_price(self, obj: ProductSale) -> float:
        return obj.product.price

    def get_salePrice(self, obj: ProductSale) -> float:
        return obj.salePrice

    def get_title(self, obj: ProductSale) -> str:
        return obj.product.title

    def get_dateFrom(self, obj: ProductSale) -> str:
        return str(obj.dateFrom)[5:]

    def get_dateTo(self, obj: ProductSale) -> str:
        return str(obj.dateFrom)[5:]

    def get_images(self, obj: ProductSale):
        product_image = ProductImage.objects.get(product=obj.product)

        return [
            {
                "src": f"{product_image.src.url}",
                "alt": f"{product_image.alt}"
            }
        ]

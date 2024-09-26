from django.utils import timezone

from django.urls import reverse
from rest_framework.test import APITestCase

from product.models import Product, Category, ProductImage, Tag
from sale.models import ProductSale


class CatalogAPITest(APITestCase):

    def setUp(self):

        self.category = Category.objects.create(title="Category test title")
        self.tag = Tag.objects.create(name="BEST")

        self.product = Product.objects.create(
            title="Title test product",
            price=2.2,
            category=self.category,
            count=5,
        )
        self.product.tags.add(self.tag)
        self.product.save()

        self.product_image = ProductImage.objects.create(
            product=self.product,
            src="products/product_16/images/Красная_роза.jpg",
            alt="Alternative text for the image"
        )
        self.product_sale = ProductSale.objects.create(
            product=self.product,
            salePrice=55.5,
            dateFrom=timezone.datetime(2020, 5, 22),
            dateTo=timezone.datetime(2020, 5, 22),
        )

    def test_get_catalog_200(self):
        """Получение 200 ответа от каталога"""

        response = self.client.get(
            path=reverse("catalog:catalog-list"),
            data={
                "filter[freeDelivery]": True,
                "filter[minPrice]": 0,
                "filter[maxPrice]": 0,
                "filter[name]": "",
                "sort": "title",
                "sortType": "inc",
                "currentPage": 1
            }
        )

        self.assertEqual(response.status_code, 200)

from _decimal import Decimal
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from product.models import Product, Category, ProductImage
from sale.models import ProductSale


class ProductSaleTest(APITestCase):
    """Тестирование страницы товаров со скидками."""

    def setUp(self):

        self.category = Category.objects.create(title="Category test title")
        self.product = Product.objects.create(
            title="Title test product",
            price=2.2,
            category=self.category,
            count=5
        )
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
        self.url = reverse("sale:sale")

        self.data = {
            "title": self.product.title,
            "price": str(self.product.price),
            "old_price": str(self.product_sale.salePrice),
            "image": self.product_image.src.url,
            "category": self.category.title,
            "date_from": self.product_sale.dateFrom.strftime("%Y-%m-%d"),
            "date_to": self.product_sale.dateTo.strftime("%Y-%m-%d"),
        }

    def tearDown(self):
        self.category.delete()
        self.product.delete()
        self.product_image.delete()
        self.product_sale.delete()

    def test_get_response_200(self):
        """Тестирование 200 ответа от GET запроса к странице sale."""

        response = self.client.get(self.url, {"currentPage": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_content(self):
        """Тестирование контента в ответе GET-запроса к странице sale."""

        response = self.client.get(self.url, {"currentPage": 1})
        data = response.data["items"][0]

        self.assertEqual(data["title"], self.data["title"])
        self.assertEqual(data["price"], Decimal(self.data["price"]))

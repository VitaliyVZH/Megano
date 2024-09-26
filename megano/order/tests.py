from django.contrib.auth.models import User
from django.test import Client, TestCase
from decimal import Decimal

from django.urls import reverse

from profiles.models import UserProfile
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from product.models import Product, Category, Tag, Reviews, Specifications


class OrderModelTest(TestCase):
    """Тесты для модели Order."""

    def setUp(self):
        """Создание объектов для тестирования."""

        # Создаем пользователя
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Создаем профиль пользователя
        self.user.profile = UserProfile.objects.create(user=self.user, fullName="Test User", email="test@example.com", phone="1234567890")

        # Создаем категорию для товара
        self.category = Category.objects.create(title="Test Category")

        # Создаем тег для товара
        self.tag = Tag.objects.create(name="Test Tag")

        # Создаем товар с необходимыми параметрами
        self.product = Product.objects.create(
            title="Test Product",
            price=100.00,
            category=self.category,
            count=10,
            description="Test Description",
            fullDescription="Test Full Description",
            freeDelivery=True,
            rating=4.5
        )
        # Добавляем к товару тег
        self.product.tags.add(self.tag)

        # Создаем спецификацию для товара и устанавливаем поле specifications
        self.specifications = Specifications.objects.create(
            name="Тестовая спецификация",
            value="Тестовое значение",
            specifications=self.product
        )

        # Создаем отзывы о товаре
        self.review1 = Reviews.objects.create(
            reviewer=self.user,
            author="Test Author",
            product=self.product,
            email="test@example.com",
            text="Test Review 1",
            rate=5
        )
        self.review2 = Reviews.objects.create(
            reviewer=self.user,
            author="Test Author",
            product=self.product,
            email="test@example.com",
            text="Test Review 2",
            rate=4
        )

        # Создаём заказ
        self.order = Order.objects.create(
            profile=self.user.profile,
            deliveryType="Delivery",
            paymentType="Online card",
            totalCost=200.00,
            status="Accepted",
            city="Test City",
            address="Test Address"
        )

        # Создаем товары в заказе
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("100.00"),
            quantity=2
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("100.00"),
            quantity=1
        )

    def test_order_model(self):
        """Тесты для модели Order."""

        # Проверяем, что заказ был создан правильно
        self.assertEqual(self.order.profile, self.user.profile)
        self.assertEqual(self.order.deliveryType, "Delivery")
        self.assertEqual(self.order.paymentType, "Online card")
        self.assertEqual(self.order.totalCost, 200.00)
        self.assertEqual(self.order.status, "Accepted")
        self.assertEqual(self.order.city, "Test City")
        self.assertEqual(self.order.address, "Test Address")

        # Проверяем, что товары в заказе были созданы правильно
        self.assertEqual(self.order_item1.order, self.order)
        self.assertEqual(self.order_item1.product, self.product)
        self.assertEqual(self.order_item1.price, 100.00)
        self.assertEqual(self.order_item1.quantity, 2)

        self.assertEqual(self.order_item2.order, self.order)
        self.assertEqual(self.order_item2.product, self.product)
        self.assertEqual(self.order_item2.price, 100.00)
        self.assertEqual(self.order_item2.quantity, 1)

    def test_order_serializer(self):
        """Тесты для сериализатора OrderSerializer."""

        # Сериализуем заказ
        serializer = OrderSerializer(self.order)

        # Проверяем, что данные сериализованы правильно
        self.assertEqual(serializer.data["id"], self.order.pk)
        self.assertIsNotNone(serializer.data["createdAt"])
        self.assertEqual(serializer.data["fullName"], self.user.profile.fullName)
        self.assertEqual(serializer.data["email"], self.user.profile.email)
        self.assertEqual(serializer.data["phone"], self.user.profile.phone)
        self.assertEqual(serializer.data["deliveryType"], self.order.deliveryType)
        self.assertEqual(serializer.data["paymentType"], self.order.paymentType)
        self.assertEqual(serializer.data["totalCost"], str(self.order.totalCost))
        self.assertEqual(serializer.data["status"], self.order.status)
        self.assertEqual(serializer.data["city"], self.order.city)
        self.assertEqual(serializer.data["address"], self.order.address)

        # Проверяем, что товары в заказе сериализованы правильно
        products_data = serializer.data["products"]
        self.assertEqual(products_data[0]["pk"], self.order_item1.pk)
        self.assertEqual(products_data[0]["order"], self.order.pk)
        self.assertEqual(products_data[0]["product"]["id"], self.product.pk)
        self.assertEqual(products_data[1]["price"], '{:.2f}'.format(self.order_item2.price))

        self.assertEqual(products_data[0]["quantity"], self.order_item1.quantity)

        self.assertEqual(products_data[1]["pk"], self.order_item2.pk)
        self.assertEqual(products_data[1]["order"], self.order.pk)
        self.assertEqual(products_data[1]["product"]["id"], self.product.pk)
        self.assertEqual(products_data[1]["price"], str(self.order_item2.price))
        self.assertEqual(products_data[1]["quantity"], self.order_item2.quantity)

    def test_order_item_serializer(self):
        """Тесты для сериализатора OrderItemSerializer."""

        # Сериализуем товар в заказе
        serializer = OrderItemSerializer(self.order_item1)

        # Проверяем, что данные сериализованы правильно
        self.assertEqual(serializer.data["pk"], self.order_item1.pk)
        self.assertEqual(serializer.data["order"], self.order.pk)
        self.assertEqual(serializer.data["product"]["id"], self.product.pk)
        self.assertEqual(serializer.data["price"], str(self.order_item1.price))
        self.assertEqual(serializer.data["quantity"], self.order_item1.quantity)

    def test_order_view(self):
        """Тесты для OrderView."""

        # Получаем клиента для выполнения запросов к серверу
        client = Client()

        # Аутентифицируем пользователя
        client.login(username=self.user.username, password='testpass')

        # Делаем POST-запрос к OrderView
        response = client.post(
            reverse("order:order"),
            data=[
                {
                    "id": self.product.pk,
                    "count": 2,
                    "price": str(self.product.price)
                },
                {
                    "id": self.product.pk,
                    "count": 1,
                    "price": str(self.product.price)
                }
            ],
            content_type="application/json",
        )

        # Проверяем, что ответ сервера содержит ID созданного заказа
        self.assertIn("orderId", response.data)
        self.assertIsNotNone(response.data["orderId"])

        # Проверяем, что заказ был создан в базе данных
        order = Order.objects.get(pk=response.data["orderId"])
        self.assertIsNotNone(order)

        # Проверяем, что товары в заказе были созданы правильно
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(order_items.count(), 2)
        self.assertEqual(order_items[0].product, self.product)
        self.assertEqual(order_items[0].price, self.product.price * 2)
        self.assertEqual(order_items[0].quantity, 2)

        self.assertEqual(order_items[1].product, self.product)
        self.assertEqual(order_items[1].price, self.product.price * 1)
        self.assertEqual(order_items[1].quantity, 1)

    def test_order_details_view(self):
        """Тесты для OrderDetailsView."""

        # Получаем клиента для выполнения запросов к серверу
        client = Client()

        # Аутентифицируем пользователя
        client.login(username=self.user.username, password='testpass')

        # Делаем GET-запрос к OrderDetailsView
        response = client.get(reverse("order:order_details", kwargs={"pk": self.order.pk}))

        # Проверяем, что ответ сервера содержит данные заказа
        self.assertEqual(response.data["pk"], self.order.pk)
        self.assertEqual(response.data["createdAt"], self.order.createdAt)
        self.assertEqual(response.data["fullName"], self.user.profile.fullName)
        self.assertEqual(response.data["email"], self.user.profile.email)
        self.assertEqual(response.data["phone"], self.user.profile.phone)
        self.assertEqual(response.data["deliveryType"], self.order.deliveryType)
        self.assertEqual(response.data["paymentType"], self.order.paymentType)
        self.assertEqual(response.data["totalCost"], float(self.order.totalCost))
        self.assertEqual(response.data["status"], self.order.status)
        self.assertEqual(response.data["city"], self.order.city)
        self.assertEqual(response.data["address"], self.order.address)


from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from profiles.models import UserProfile
from .models import Product, Category, Tag, Reviews, Specifications
from .serializers import ProductDetailSerializer, ReviewSerializer


class TagTests(TestCase):
    """Тест тегов товаров."""

    def setUp(self) -> None:
        """Создание данных, используемых при тестировании."""

        self.tag_name = "Test tag"
        self.tag = Tag.objects.create(name=self.tag_name)

    def tearDown(self) -> None:
        self.tag.delete()

    def test_get_tag_200(self):
        """Получение 200 ответа от GET запроса к product_tags."""

        response = self.client.get(reverse("product:product_tags"))
        self.assertEqual(response.status_code, 200)

    def test_content_tag(self):
        """Проверка контента тега (имени тега)."""

        response = self.client.get(reverse("product:product_tags"))
        self.assertEqual(response.data[0]["name"], self.tag_name)


class ProductTest(TestCase):
    """Тест страниц с деталировкой товаров."""
    def setUp(self):
        """Создание объектов для тестирования."""

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

        # Создаем пользователя
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Создаем профиль пользователя
        self.user.profile = UserProfile.objects.create(user=self.user)

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

    def test_product_detail_page(self):
        """Тест страницы товара."""

        # Получаем клиента для выполнения запросов к серверу.
        client = Client()

        # Делаем GET-запрос к странице товара.
        response = client.get(reverse("product:product_details", kwargs={"pk": self.product.pk}))

        # Проверяем, что страница товара возвращает статус 200 (OK).
        self.assertEqual(response.status_code, 200)

        # Сериализуем данные товара с помощью сериализатора ProductDetailSerializer.
        product_serializer = ProductDetailSerializer(self.product)

        # Проверяем, что данные, полученные в ответе от сервера, совпадают с данными,
        # сериализованными с помощью сериализатора.
        self.assertEqual(response.data, product_serializer.data)

        # Проверяем, что все отзывы товара отображаются правильно.
        reviews_serializer = ReviewSerializer([self.review1, self.review2], many=True)
        self.assertEqual(response.data["reviews"], reviews_serializer.data)

        # Проверяем, что средний рейтинг товара рассчитывается правильно, основываясь на отзывах.
        self.assertAlmostEqual(float(response.data["rating"]), (self.review1.rate + self.review2.rate) / 2, places=1)

    def test_add_review(self):
        """Тест добавления отзыва к товару."""

        client = Client()
        # Аутентифицируем пользователя.
        client.login(username=self.user.username, password='testpass')

        response = client.post(
            reverse("product:product_reviews", kwargs={"pk": self.product.pk}),
            data={
                "author": self.user.username,
                "email": "test@example.com",
                "text": "Test Review 3",
                "rate": 5
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["author"], "Test Author")
        self.assertEqual(response.data[0]["email"], "test@example.com")
        self.assertEqual(response.data[-1]["text"], "Test Review 3")
        self.assertEqual(response.data[0]["rate"], 5)

        # Проверка, был ли добавлен отзыв к товару.
        product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(product.reviews.count(), 3)

        # Проверка, обновился ли рейтинг продукта.
        self.assertAlmostEqual(float(product.rating), (self.review1.rate + self.review2.rate + 5) / 3, places=1)

    def test_add_review_unauthenticated(self):
        """Тест добавления отзыва к товару не аутентифицированного пользователя."""

        client = Client()
        # Аутентифицируем пользователя.

        response = client.post(
            reverse("product:product_reviews", kwargs={"pk": self.product.pk}),
            data={
                "author": self.user.username,
                "email": "test@example.com",
                "text": "Test Review 3",
                "rate": 5
            },
            content_type="application/json",
        )

        # Проверка на попытку оставить отзыв не авторизованного пользователя
        self.assertEqual(response.status_code, 403)

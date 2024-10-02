from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from order.models import Order
from payment.models import Payment
from profiles.models import UserProfile

from rest_framework.test import APIClient


class PaymentTest(TestCase):

    def setUp(self):
        """Создание объектов для тестирования."""

        # Создание пользователя
        self.user = User.objects.create(
            username="User_test",
            password="password_test"
        )

        # Создание профиля пользователя
        self.profile_user = UserProfile.objects.create(
            user=self.user,
            fullName=self.user.username,
            phone="3332221155",
            email="qwerty@yandex.ru",
        )

        # Создание заказа
        self.order = Order.objects.create(
            profile=self.profile_user,
            totalCost=55.5,
            city="test_city",
            address="test_address",
            deliveryType="Express delivery",

        )

        # Создание платежа и установка внешнего ключа для заказа
        self.payment = Payment.objects.create(
            number="1234567890123456",
            name="Test Card",
            code="123",
            year="2025",
            payment_user_profile=self.profile_user,
            payment_num_orders=self.order
        )

    def test_get_payment(self):
        """Получение 200 ответа от PaymentAPIView."""

        client = APIClient()
        data = {
            "name": "Test Card",
            "code": "123",
            "year": "2025",
            "number": "1234567890123456"
        }
        response = client.post(reverse("payment:payment-detail"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_payment_data(self):
        """Проверка валидности данных имени."""

        client = APIClient()
        data = {
            "name": "",  # Не валидные данные
            "code": "123",
            "year": "2025",
            "number": "1234567890123456"
        }
        response = client.post(reverse("payment:payment-detail"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

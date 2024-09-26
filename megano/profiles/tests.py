
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from profiles.models import UserProfile, UserAvatar


class ProfileTests(APITestCase):
    """В классе ProfileTests реализованы тесты относящиеся к профилю пользователя."""
    def setUp(self) -> None:
        """В методе setUp создаются объекты, необходимые для тестирования представлений."""

        self.user = User.objects.create(
            username="username Test Name",
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email@.com",
            password="Test Password"
        )
        self.user.save()

        self.profile = UserProfile.objects.create(
            fullName="".join((self.user.first_name, " ", self.user.last_name)),
            phone="+79373332211",
            email=self.user.email,
            user=self.user
        )

        self.user_avatar = UserAvatar.objects.create(
            src="products/product_16/images/Красная_роза.jpg",
            alt="test_alt_avatar",
            user=self.user,
            user_profile=self.profile,
        )
        self.user_avatar.save()

        self.url = reverse("profiles:user_profile")

    def test_get_response_200(self):
        """Тестирование 200 ответа от GET запроса к странице profile."""

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_profile_post(self):
        """Тестирование POST запроса на изменение данных профиля пользователя."""

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
              "fullName": "Annoying Orange",
              "email": "no-reply@mail.ru",
              "phone": "88002000600",
              "avatar": {
                "src": "products/product_16/images/Красная_роза.jpg",
                "alt": "Image alt string"
              }
            }, format="json")

        self.assertEqual(response.status_code, 200)

    def test_change_password_user_profile(self):
        """Тестирование изменения пароля профиля пользователя."""

        user = self.client.login(username=self.user.username, password=self.user.password)

        self.assertIsNotNone(user)
        self.client.force_authenticate(user=self.user)

        new_password = "newPass321!!!"
        response = self.client.post(
            path=self.url,
            data={
                "currentPassword": self.user.password,
                "newPassword": new_password,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)

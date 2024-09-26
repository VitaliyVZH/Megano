import json

from django.contrib.auth.models import User, Group

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class MyAuthTests(APITestCase):

    def setUp(self) -> None:

        self.data_user = {
            "username": "TestUsername",
            "first_name": "TestFirstname",
            "password": "TestPassword",
        }

        self.user = User.objects.create_user(
            username=self.data_user["username"],
            password=self.data_user["password"]
        )

        Group.objects.create(name="authorized_user")

    def tearDown(self) -> None:
        """
        Функция tearDown запускается автоматически после отработки всех тестов,
        в ней реализован функционал удаления всех ранее созданных объектов.
        """

        self.user.delete()  # удаление созданного пользователя

    def tests_register_user_response_200(self):
        """Тест на регистрацию нового пользователя с получением 200 ответа."""

        response = self.client.post(
            path=reverse("myauth:user_register"),
            data=json.dumps(self.data_user).encode("utf-8"),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)

    def tests_sign_in_response_200(self):
        """Тест входа пользователя в свой аккаунт."""

        url = reverse("myauth:user_login")
        response = self.client.post(
            path=url,
            data={
                "username": self.data_user["username"],
                "password": self.data_user["password"],
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

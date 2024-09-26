import json

from django.contrib.auth.models import User
from django.http import QueryDict
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    class Meta:
        model = User
        fields = "username", "first_name", "password",

    def to_internal_value(self, data):

        if type(data) is not QueryDict:  # для тестирования
            cleaned_data = data.copy()
        else:
            cleaned_data = json.loads(list(data)[0])
            cleaned_data["first_name"] = cleaned_data["name"]
            del cleaned_data["name"]
        return cleaned_data


class UserSignInSerializer(serializers.ModelSerializer):
    """Сериализатор для аутентификации пользователя"""

    class Meta:
        model = User
        fields = "username", "password",

    def to_internal_value(self, data):
        """Функция преобразовывает данные в словарь."""

        cleaned_data = json.loads(list(data)[0])
        return cleaned_data

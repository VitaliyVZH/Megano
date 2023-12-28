import json

from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации и аутентификации пользователя"""

    class Meta:
        model = User
        fields = "username", "first_name", "password",

    def to_internal_value(self, data):
        """Функция меняет ключ, если такой есть"""

        cleaned_data = json.loads(list(data)[0])
        if cleaned_data.get("name"):
            cleaned_data["first_name"] = cleaned_data["name"]
            del cleaned_data["name"]
            return cleaned_data
        return cleaned_data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "",

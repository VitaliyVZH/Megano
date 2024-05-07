import json

from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import UserProfile, UserAvatar


class UserAvatarSerializer(serializers.ModelSerializer):
    """Сериализатор обрабатывает данные модели UserAvatar (аватарки пользователя)."""

    class Meta:
        model = UserAvatar
        fields = "src", "alt"


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели UserProfile (профиля пользователя), в нём дополнительно
    обрабатывается вложенный сериализатор 'avatar'.
    """

    avatar = UserAvatarSerializer()

    class Meta:
        model = UserProfile
        fields = "fullName", "phone", "email", "avatar"


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обрабатывает данные профиля пользователя для дальнейшего из обновления."""

    class Meta:
        model = UserProfile
        fields = "fullName", "phone", "email",

    def update(self, instance, validated_data):
        """
        Функция обновляет данные профиля пользователя.
        Функция update отрабатывает при вызове функции save() во View, в методе POST, при этом в сериализатор
        обязательно должен передаваться instance объекта.
        """

        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.fullName = validated_data.get("fullName", instance.fullName)
        instance.save()
        return instance


class UserPasswordSerializer(serializers.ModelSerializer):
    newPassword = serializers.CharField()

    class Meta:
        model = User
        fields = "password", "newPassword"

    def to_internal_value(self, data):
        data["password"] = data["currentPassword"]
        del data["currentPassword"]
        return data

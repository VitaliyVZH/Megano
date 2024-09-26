
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

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "fullName", "phone", "email", "avatar"

    def get_avatar(self, obj: UserProfile):
        user_avatar = UserAvatar.objects.get(user_profile=obj)
        serializer = UserAvatarSerializer(user_avatar)
        return serializer.data


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
    newPassword = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = "password", "newPassword"

    def to_internal_value(self, data):
        data = data.copy()  # Создаём копию данных, чтобы избежать изменения оригинального QueryDict
        data["password"] = data["currentPassword"]
        del data["currentPassword"]
        return data

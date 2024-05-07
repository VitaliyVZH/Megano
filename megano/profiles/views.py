from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import UserProfile, UserAvatar
from profiles.serializers import UserProfileSerializer, UserProfileUpdateSerializer, UserPasswordSerializer


class UserProfileAPIView(APIView):
    """
    Класс реализует:
     - отображение информации содержащуюся в профиле пользователя;
     - изменение информации профиля пользователя.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Метод GET отдаёт сериализованные данные профиля пользователя."""

        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        В методе POST происходит:
         - десериализация полученных данных;
         - проверка данных на валидность, в случае успеха, сохранение данных.
         """

        serializer = UserProfileUpdateSerializer(data=request.data, instance=request.user.userprofile)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status.HTTP_400_BAD_REQUEST)


class UserAvatarApiView(APIView):
    """Класс реализует обновление аватара пользователя"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Метод получает объект аватара пользователя, сохраняет путь и описание аватара, при вызове метода save()
        в models.py вызывается одноименная функция, в которой происходит удаление предыдущей аватарки,
        если таковая имелась.
        """

        user_avatar = UserAvatar.objects.get(user=request.user)
        user_avatar.src = request.FILES["avatar"]
        user_avatar.alt = str(request.FILES["avatar"]).split(".")[0]
        user_avatar.save()
        return Response(status=status.HTTP_200_OK)


class UserPasswordAPIView(APIView):
    """Класс реализует возможность изменения пароля"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Метод POST проверяет полученные данные, если введённый пароль равен существующему,
        а новый пароль соответствует требованиям, тогда новый пароль сохраняется
        """
        
        serializer = UserPasswordSerializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data["password"]
            # при помощи аутентификации проверяем пароль который ввел пользователь (его ли это пароль)
            user = authenticate(username=request.user.username, password=password)
            if user:
                new_password = serializer.validated_data["newPassword"]
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)


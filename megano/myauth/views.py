
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import Group, User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth.serializers import UserSerializer
from profiles.models import UserProfile, UserAvatar


class UserLoginApiView(APIView):
    """Аутентификация пользователя."""

    def post(self, request: Request) -> Response:

        serializer = UserSerializer(data=request.data)  # десереализация данных

        if serializer.is_valid():  # если данные валидны ниже получим их
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutApiView(APIView):
    """Выход пользователя из учетной записи."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserRegisterApiView(APIView):
    """Регистрация нового пользователя."""

    def post(self, request: Request) -> Response:
        serialized = UserSerializer(data=request.data)  # десериализация данных
        if serialized.is_valid():

            password = serialized.validated_data["password"]
            username = serialized.validated_data["username"]
            first_name = serialized.validated_data["first_name"]

            # создание нового пользователя
            user = User.objects.create(password=password, username=username, first_name=first_name)

            user.set_password(password)  # шифрование пароля

            avatar = UserAvatar.objects.create(user=user)  # создание поля для аватара пользователя
            UserProfile.objects.create(user=user, avatar=avatar)  # создание профиля пользователя

            group = Group.objects.get(name="authorized_user")  # добавление группы
            user.groups.add(group)
            user.save()

            login(request, user)  # вход в учетную запись

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

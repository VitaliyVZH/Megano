
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import Group, User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth.serializers import UserSerializer, UserSignInSerializer
from profiles.models import UserProfile, UserAvatar


class UserLoginApiView(APIView):
    """Аутентификация пользователя."""

    def post(self, request: Request) -> Response:
        """
        Функция POST десереализует данные, проверяет их на валидность и аутентифицирует пользователя,
        если данные валидны.
        """

        serializer = UserSignInSerializer(data=request.data)  # десереализация данных

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
        """Функция POST разлогинивает пользователя."""

        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserRegisterApiView(APIView):
    """Регистрация нового пользователя."""

    def post(self, request: Request) -> Response:
        """
        Регистрация пользователя.
        Функция POST десереализует данные, проверяет их на валидность и если данные валидны создаёт:
          - пользователя;
          - профиль пользователя;
          - аватар;
          - добавляет пользователя в группу;
          - входит в аккаунт пользователя.
        """

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                first_name=serializer.validated_data["first_name"],
                password=serializer.validated_data["password"]
            )
            user_profile = UserProfile.objects.create(user=user)
            UserAvatar.objects.create(user=user, user_profile=user_profile)
            group = Group.objects.get(name="authorized_user")
            user.groups.add(group)
            user.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

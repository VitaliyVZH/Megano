from django.urls import path

from myauth.views import UserLoginApiView, UserLogoutApiView, UserRegisterApiView

app_name = "myauth"


urlpatterns = [
    path("sign-in", UserLoginApiView.as_view(), name="user_login"),        # аутентификация пользователя
    path("sign-out", UserLogoutApiView.as_view(), name="user_logout"),     # выход пользователя из учетной записи
    path("sign-up", UserRegisterApiView.as_view(), name="user_register"),  # регистрация пользователя
]

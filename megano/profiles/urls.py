from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from profiles.views import UserProfileAPIView, UserAvatarApiView, UserPasswordAPIView

app_name = "profiles"


urlpatterns = [
    path("profile", UserProfileAPIView.as_view()),
    path("profile/avatar", UserAvatarApiView.as_view()),
    path("profile/password", UserPasswordAPIView.as_view()),
]

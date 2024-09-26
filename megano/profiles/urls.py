from django.urls import path

from profiles.views import UserProfileAPIView, UserAvatarApiView, UserPasswordAPIView

app_name = "profiles"


urlpatterns = [
    path("profile", UserProfileAPIView.as_view(), name="user_profile"),
    path("profile/avatar", UserAvatarApiView.as_view(), name="profile_avatar"),
    path("profile/password", UserPasswordAPIView.as_view(), name="profile_password"),
]

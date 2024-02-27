
from django.contrib import admin
from django.utils.safestring import mark_safe

from profiles.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Реализация административной панели профайла пользователя"""

    list_display = "pk", "fullName", "phone", "email", "get_avatar"
    list_display_links = "pk", "fullName"
    ordering = "pk",
    fields = "user", "fullName", "phone", "email", "avatar"

    def get_queryset(self, request):
        return UserProfile.objects.prefetch_related("user")

    def get_avatar(self, obj):
        if not obj.avatar.src:
            return f"No avatar"
        return mark_safe(f'<img src={obj.avatar.src.url}>')

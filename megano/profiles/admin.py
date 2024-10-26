
from django.contrib import admin
from django.utils.safestring import mark_safe

from profiles.models import UserProfile, UserAvatar


class UserAvatarInline(admin.TabularInline):
    model = UserAvatar
    fields = "src", "alt", "avatar"
    readonly_fields = "avatar",

    def avatar(self, obj: UserAvatar):
        return mark_safe(f'<img src={obj.src.url} width="90" height="90"')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Реализация административной панели профайла пользователя"""

    inlines = [
        UserAvatarInline,
    ]

    list_display = "pk", "fullName", "phone", "email", "get_avatar",
    list_display_links = "pk", "fullName"
    ordering = "pk",
    fields = "user", "fullName", "phone", "email",

    def get_queryset(self, request):
        """Подгрузка связанных таблиц"""

        return UserProfile.objects.prefetch_related("user")

    def get_avatar(self, obj: UserProfile):
        avatar = UserAvatar.objects.get(user_profile=obj)
        if not avatar.src:
            return f"No avatar"
        else:
            return mark_safe(f'<img src={avatar.src.url}>')

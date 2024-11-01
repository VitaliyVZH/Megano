from django.contrib.auth.models import User
from django.db import models


def path_avatar(instance: "User", filename: str) -> str:
    """Функция возвращает путь к месту хранению файла (изображения) пользователя."""
    return f"image_user/user_{instance.user.pk}/{filename}"


class UserProfile(models.Model):
    """Модель профиля пользователя."""

    fullName = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"Profile: {self.user.username}, profile #{self.pk}"


class UserAvatar(models.Model):
    """Модель аватара пользователя."""

    src = models.ImageField(null=True, blank=True, upload_to=path_avatar)
    alt = models.CharField(blank=True, max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Функция save() отрабатывает при сохранении аватарки пользователя, функция проверяет наличие
        ранее сохранённого файла, если такой имеется, он удаляется и сохраняется добавленный файл.
        """

        if self.pk:
            old_self = UserAvatar.objects.filter(pk=self.pk, user=self.user).first()
            if old_self and self.src != old_self.src:
                old_self.src.delete(False)
        return super().save(*args, **kwargs)

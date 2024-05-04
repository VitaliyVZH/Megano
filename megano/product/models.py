import os
import shutil

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def product_image_path(instance: "ProductImage", filename: str) -> str:
    """Функция создаёт папки для хранения фотографий товаров"""

    return f"products/product_{instance.product.pk}/images/{filename}"


class Product(models.Model):
    """Класс Product реализует модель (таблицу) товара"""

    title = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=False)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING, blank=False)
    count = models.PositiveIntegerField(default=0, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=400, blank=True)
    fullDescription = models.CharField(max_length=1000, blank=True)
    freeDelivery = models.BooleanField(default=False, blank=True)
    rating = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    tags = models.ManyToManyField("Tag", related_name="products")

    def __str__(self):
        return f"#{self.pk}. {self.title}"


class ProductImage(models.Model):
    """Класс ProductImage реализует модель (таблицу) для фотографий товара"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    src = models.ImageField(upload_to=product_image_path)
    alt = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Product photo: {self.product.title}"


class Tag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"


class Reviews(models.Model):
    """Класс Reviews реализует модель (таблицу) для отзывов товара"""

    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    email = models.EmailField()
    text = models.TextField(blank=True, max_length=500)
    rate = models.IntegerField(
        default=0,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Review from user {self.author} about the {self.product}"


class Specifications(models.Model):
    """Класс Specifications реализует модель (таблицу) со спецификацией товара"""

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=10)
    specifications = models.OneToOneField(Product, on_delete=models.CASCADE)


def category_directory_path(instance: "Category", filename: str) -> str:
    """Создание пути в файловой системе к месту хранения файла"""

    # получение абсолютного пути к папке с фотографией категории
    path = os.path.abspath(os.path.join("uploads", f"categories/{instance.title}"))
    # если папка этой категории уже существует
    if os.path.isdir(path):
        # удаляем её
        shutil.rmtree(path)
    # возвращаем путь, по которому будет сохранена новая фотография
    return f"categories/{instance.title}/{filename}"


class Category(models.Model):
    """Класс Category реализует модель (таблицу) с категориями товаров которые есть в интернет магазине"""

    class Meta:
        ordering = "title",

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=category_directory_path)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"#{self.pk}. {self.title}"


import datetime
from statistics import mean, StatisticsError

from rest_framework import serializers

from product.models import Product, Category
from product.serializers import ImageProductSerializer, TagSerializer


class CatalogSerializer(serializers.ModelSerializer):
    """Сериализатор обрабатывает данные модели Product."""

    images = ImageProductSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Product

        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating"
        ]

    def get_reviews(self, obj):
        return len(obj.reviews.all())

    def get_rating(self, obj):
        rate = [i.rate for i in obj.reviews.all()]
        if rate:
            return round(sum(rate) / len(rate), 1)
        return 0.0

    def to_representation(self, obj):

        tz = datetime.timezone(datetime.timedelta(hours=1), name="Central European Standard Time")
        gmt_timezone = obj.date.astimezone(tz).strftime('%a %b %d %Y %X GMT%z (%Z)')

        try:
            review = round(mean([review.rate for review in obj.reviews.all()]), 1)
        except StatisticsError:
            review = 0.0

        return {
            "id": obj.id,
            "category": obj.category_id,
            "price": obj.price,
            "count": obj.count,
            "date": gmt_timezone,
            "title": obj.title,
            "description": obj.description,
            "freeDelivery": obj.freeDelivery,
            "images": [{"src": str(img_obj.src.url), "alt": img_obj.alt} for img_obj in obj.images.all()],
            "tags": [{"id": tag_obj.pk, "name": tag_obj.name} for tag_obj in obj.tags.all()],
            "reviews": review,
            "rating": obj.rating,
        }


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

    def to_representation(self, obj):
        all_cat = Category.objects.all()

        def search_subcategories(parent_cat_id: int) -> list:
            """
            Функция search_subcategories возвращает список с вложенными словарями, в словарях данные о
            категориях и подкатегориях товаров.
            Функция проверяет наличие дочерних категорий у родительской категории,
            при наличии дочерней категории, она добавляется в родительскую подкатегорию
            """

            # создаём список для хранения данных подкатегорий
            cat_list = []

            # из таблицы с категориями товаров по id родительской категории получаем список (QuerySet)
            # с возможными подкатегориями
            list_parent_cat_obj = all_cat.filter(parent_category=parent_cat_id)

            # если полученный список с подкатегориями не пустой
            if list_parent_cat_obj:
                # переберём его
                for cat in list_parent_cat_obj:
                    # каждую подкатегорию добавим в ранее созданный список cat_list
                    cat_list.append(
                        {
                            "pk": cat.pk,
                            "title": cat.title,
                            "image": {
                                "src": str(cat.image.url),
                                "alt": cat.title,
                            },
                            # для каждой подкатегории вызываем функцию поиска подкатегории
                            "subcategories": search_subcategories(parent_cat_id=cat.pk),
                        }
                    )
                return cat_list
            return cat_list

        # возвращается результат главной функции to_representation
        return {
                "pk": obj.pk,
                "title": obj.title,
                "image": {
                    "src": str(obj.image.url),
                    "alt": obj.title,
                },
                "subcategories": search_subcategories(parent_cat_id=obj.pk),
            }
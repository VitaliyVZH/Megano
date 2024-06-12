import datetime

from rest_framework import serializers

from product.models import Product, ProductImage, Tag, Reviews, Specifications


class ImageProductSerializer(serializers.ModelSerializer):
    """Сериализатор ImageProductSerializer возвращает данные (фото товара) в JSON формате."""

    class Meta:
        model = ProductImage
        fields = "src", "alt"


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор TagSerializer возвращает данные (теги товара) в JSON формате."""

    class Meta:
        model = Tag
        fields = "pk", "name",


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор ReviewSerializer возвращает данные (отзывы о товаре) в JSON формате."""

    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reviews
        fields = "author", "email", "text", "rate", "date"

    def get_date(self, obj: Reviews) -> str:
        return obj.date.strftime('%Y-%m-%d %I:%M')


class SpecificationsSerializer(serializers.ModelSerializer):
    """Сериализатор SpecificationsSerializer возвращает данные (спецификация товара) в JSON формате."""

    class Meta:
        model = Specifications
        fields = "name", "value",


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор ProductDetailSerializer возвращает данные (данные товара) в JSON формате."""

    date = serializers.SerializerMethodField()
    images = ImageProductSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

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
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating"
        ]

    def get_date(self, obj: Product) -> str:
        """Функция get_date возвращает дату в требуемом формате."""

        tz = datetime.timezone(datetime.timedelta(hours=1), name="Central European Standard Time")
        gmt_timezone = obj.date.astimezone(tz).strftime('%a %b %d %Y %X GMT%z (%Z)')
        return gmt_timezone

    def get_specifications(self, obj: Product) -> list[dict]:
        """Функция get_specifications отдаёт данные о спецификации товара в списке."""

        return [
            {
                "name": obj.specifications.name,
                "value": obj.specifications.value
            }
        ]

    def get_rating(self, obj: Product) -> float:
        """Функция get_rating возвращает среднюю оценку товара."""

        rate = [rev.rate for rev in obj.reviews.all()]
        if rate:
            return round(sum(rate) / len(rate), 1)
        return 0.0

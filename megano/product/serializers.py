
from rest_framework import serializers

from product.models import Product, ProductImage, Tag, Reviews


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор обрабатывает данные модели Product."""

    images = ProductImage()
    tags = Tag()
    reviews = Reviews()

    class Meta:
        model = Product
        fields = [
            "pk",
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


class ImageProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "src", "alt"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "pk", "name",


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = "__all__"

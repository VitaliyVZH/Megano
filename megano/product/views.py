from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from product.models import Tag, Product, Reviews
from product.serializers import TagSerializer, ProductDetailSerializer, ReviewSerializer


class ProductDetailAPIView(RetrieveAPIView):
    """ProductDetailAPIView возвращает данные об конкретном товаре."""

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ReviewProductAPIView(ListAPIView):
    """
    ReviewProductAPIView возвращает данные об отзывах товара,
    сохраняет новые отзывы о товаре.
    """

    queryset = Product.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        # передаём данные в сериализатор для проверки на валидность
        serializer = ReviewSerializer(data=request.data)
        # если они валидные
        if serializer.is_valid():
            # получим объект товара для сохранения отзыва
            product = Product.objects.get(pk=kwargs["pk"])
            # сохраняем отзыв, передавая нужные поля
            Reviews.objects.create(
                reviewer=self.request.user,
                author=self.request.user.username,
                product=product,
                email=self.request.user.email,
                text=serializer.validated_data["text"],
                rate=serializer.validated_data["rate"],
                date=datetime.now()
            )
            # получаем список отзывов на один товар
            reviews_list = Reviews.objects.filter(product=product)
            # сериализация данных
            serializer = ReviewSerializer(reviews_list, many=True)
            # отдаём данные в битовой последовательности со статусом 200
            return Response(serializer.data, status=status.HTTP_200_OK)


class TagsListAPIView(ListAPIView):
    """TagsListAPIView возвращает данные об имеющихся тегах."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

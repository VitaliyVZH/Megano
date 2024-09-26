from datetime import datetime

from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Tag, Product, Reviews
from product.serializers import TagSerializer, ProductDetailSerializer, ReviewSerializer


class ProductDetailAPIView(RetrieveAPIView):
    """ProductDetailAPIView возвращает данные об конкретном товаре."""

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ReviewProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Добавляется новый отзыв на товар."""

        # передаём данные в сериализатор для проверки на валидность
        serializer = ReviewSerializer(data=request.data)
        # если они валидные
        if serializer.is_valid():
            # получим объект товара для сохранения отзыва
            product = Product.objects.get(pk=kwargs["pk"])

            # получаем email из профиля пользователя
            email = self.request.user.profile.email
            if not email:
                # если его нет, получаем email из введённых данных
                email = serializer.validated_data["email"]
            if email:
                # если email есть, сохраняем отзыв передавая нужные поля
                Reviews.objects.create(
                    reviewer=self.request.user,
                    author=self.request.user.username,
                    product=product,
                    email=email,
                    text=serializer.validated_data["text"],
                    rate=serializer.validated_data["rate"],
                    date=datetime.now()
                )

                # получаем список отзывов на один товар
                reviews_list = Reviews.objects.filter(product=product)

                # пересчитываем средний рейтинг товара
                product.rating = reviews_list.aggregate(Avg("rate"))["rate__avg"]
                product.save()

                # сериализация данных
                serializer = ReviewSerializer(reviews_list, many=True)
                # отдаём данные в битовой последовательности со статусом 200
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagsListAPIView(ListAPIView):
    """TagsListAPIView возвращает данные об имеющихся тегах."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

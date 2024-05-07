from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from product.models import Tag, Product
from product.serializers import ProductSerializer, TagSerializer, ProductDetailSerializer, ReviewSerializer


class ProductAPIView(APIView):
    """ProductAPIView возвращает данные о товарах"""

    def get(self, request: Request) -> Response:
        serializer = ProductSerializer(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(RetrieveAPIView):
    """ProductDetailAPIView возвращает данные об конкретном товаре"""

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ReviewProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ReviewSerializer


class TagsListAPIView(ListAPIView):
    """TagsListAPIView возвращает данные об имеющихся тегах"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

import math

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from sale.models import ProductSale
from sale.serializers import ProductSaleSerializer


class ProductSaleListAPIViewPaginator(PageNumberPagination):
    """Класс ProductSaleListAPIViewPaginator настраивает пагинацию."""

    page_size = 3  # максимальное кол-во объектов на странице
    max_page_size = 10000  # максимальное кол-во страниц


class ProductSaleListAPIView(ListAPIView):
    """Класс получает данные по продуктам со скидками и отдаются ограниченными частями согласно пагинации."""

    queryset = ProductSale.objects.all().order_by("id")
    serializer_class = ProductSaleSerializer
    pagination_class = ProductSaleListAPIViewPaginator

    def get_queryset(self):
        """Отдаёт ограниченное кол-во объектов."""

        # № текущей страницы в числовом формате
        current_page = int(self.request.query_params['currentPage'])
        # цифра, от которой будет начинаться срез объектов [start:]
        start = 0
        #  если текущая страница не является первой страницей
        if current_page != 1:
            #  тогда укажем с какого по счёту объекта начинать отдавать данные
            start = (current_page * self.pagination_class.page_size) - self.pagination_class.page_size

        return self.queryset[start:]

    def get_paginated_response(self, queryset):
        """Возвращает:
             - queryset - ограниченное кол-во данных (срез);
             - currentPage - № текущей страницы;
             - lastPage - максимальное количество страниц."""

        return Response(
            {
                "items":  queryset,
                "currentPage": self.request.query_params['currentPage'],
                "lastPage": math.ceil(len(self.queryset.all()) / self.pagination_class.page_size)
            }
        )

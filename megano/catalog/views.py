import math

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.serializers import CategoriesSerializer
from product.models import Product, Category
from product.serializers import ProductSerializer


class CatalogAPIViewPaginator(PageNumberPagination):
    """CatalogAPIViewPaginator - класс для настройки пагинации"""

    page_size = 3  # кол-во объектов на странице


class CatalogListAPIView(ListAPIView):
    """
    CatalogAPIView отдаёт данные о товарах, сортирует и фильтрует товары по параметрам пользователя
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CatalogAPIViewPaginator

    def get_queryset(self):
        """
        Функция get_queryset принимает данные о товаре и отдаёт их в отфильтрованном и
        отсортированном виде, если такие параметры были установлены пользователем.
        """

        num_products_page = self.pagination_class.page_size

        # переменная хранит в себе символ сортировки, по умолчанию символ отсутствует
        # в противном случае "-"
        symbol_order_by = ''

        # получение пользовательских настроек для сортировки и фильтрации
        param_filter = self.request.query_params

        # если параметр сортировки задан ПО УБЫВАНИЮ, присваиваем переменной symbol_order_by символ "-"
        if param_filter.get("sortType") == "inc":
            symbol_order_by = '-'

        free = param_filter.get("filter[freeDelivery]")
        if free != 'true':
            free = False
        else:
            free = True

        #  перезаписываем queryset эти же данные, только в отсортированном и отфильтрованном виде
        self.queryset = self.queryset.filter(
            price__gte=param_filter.get("filter[minPrice]"),  # price__gte сортирует данные от значения вкл-но и выше
            price__lte=param_filter.get("filter[maxPrice]"),  # price__lte сортирует данные от значения вкл-но и ниже
            freeDelivery=free

        ).order_by(f'{symbol_order_by}{param_filter["sort"]}')

        # если в параметрах фильтрации, был введён параметр поиска по имени товара, в этом случае
        # добавляем этот параметр в фильтр, изначально этот параметр приходит с пустым значением и
        # его нельзя включать в параметры фильтрации
        if param_filter["filter[name]"]:
            self.queryset = self.queryset.filter(
                title=param_filter["filter[name]"],
            )

            return self.queryset

        # переменная num_products хранит в себе кол-во отфильтрованных товаров
        num_products = len(self.queryset)

        # если кол-во отфильтрованных товаров меньше максимального количества товаров,
        # которое может отображаться на одной странице, тогда возвращается весь queryset
        if num_products <= num_products_page:
            return self.queryset

        # иначе, в переменную current_page сохраняем значение номера первого товара, который должен находиться
        # на текущей странице в соответствии с пагинацией
        current_page = (int(self.request.query_params["currentPage"]) * num_products_page) - num_products_page
        return self.queryset[current_page:]

    def get_paginated_response(self, request):
        """get_paginated_response управляет параметрами пагинации."""

        return Response(
            {
                "items": request,
                "currentPage": self.request.query_params["currentPage"],
                "lastPage": math.ceil(len(self.queryset) / self.pagination_class.page_size),
            }
        )


class CategoriesAPIView(APIView):
    """View Категорий товаров"""

    def get(self, request: Request) -> Response:
        categories = Category.objects.filter(parent_category=None)
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsPopularListAPIView(ListAPIView):
    """Представление реализует отображение популярных товаров"""

    number_displayed_products = 8
    queryset = Product.objects.order_by("pk")[:number_displayed_products]
    serializer_class = ProductSerializer


class ProductsLimitedListAPIView(ListAPIView):
    """ProductsLimitedListAPIView реализует отображение лимитированных товаров"""

    number_displayed_products = 16
    queryset = Product.objects.order_by("pk").filter(count__lte=5)[:number_displayed_products]
    serializer_class = ProductSerializer


class BannersListAPIView(ListAPIView):
    """BannersListAPIView реализует отображение лимитированных товаров"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SalesListAPIView(ListAPIView):
    """BannersListAPIView реализует отображение лимитированных товаров"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


from rest_framework.generics import ListCreateAPIView

from rest_framework.response import Response

from basket.basket import Cart

from product.models import Product
from product.serializers import ProductSerializer


def creat_basket_products(user_basket: Cart) -> list[Cart]:
    """Формирование корзины товаров."""

    basket_products = []  # список для хранения товаров

    # перебираем объекты находящиеся в классе Cart
    for prod_value in user_basket:
        # в переменной сохраняем нужный нам товар
        product = Product.objects.all().get(pk=prod_value["product_pk"])
        # указываем, какое кол-во товара
        product.count = prod_value["quantity"]

        # добавляем товар в список
        basket_products.append(product)

    return basket_products


class BasketAPIView(ListCreateAPIView):
    """Класс BasketAPIView отдаёт данные для отображения информации о корзине пользователя."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return self.list(request)

    def get_queryset(self):
        """Функция get_queryset отдаёт список с товарами (корзину)."""

        user_basket = Cart(self.request)  # создание корзины привязанной к сессии
        data = self.request.data  # хранение данных запроса от пользователя (pk и кол-во товара)

        # если были получен запрос от пользователя на добавление товаров
        if data:
            # добавление/изменение данных корзины хранимые в сессии
            user_basket.add(data["id"], data["count"])
        return creat_basket_products(user_basket)

    def delete(self, request, *args, **kwargs):

        user_basket = Cart(self.request)  # создание корзины привязанной к сессии
        data = self.request.data  # хранение данных запроса от пользователя (pk и кол-во товара)

        # если кол-во товаров у пользователя в корзине равна количеству товаров,
        # которое необходимо удалить, тогда
        if user_basket.products_quantity(data["id"]) == data["count"]:
            # вызываем функцию удаления позиции товара
            user_basket.remove(data["id"])

        else:
            # если количество единиц товаров для удаления не равно кол-ву товаров, которое
            # находится в корзине пользователя, вызываем функцию для удаления одной единицы товара
            user_basket.products_cut_count(data["id"])

        serializer = ProductSerializer(creat_basket_products(user_basket), many=True)

        return Response(serializer.data)

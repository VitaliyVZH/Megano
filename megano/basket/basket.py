"""Реализация корзины через сессию пользователя"""

from django.conf import settings

from product.models import Product


class Cart(object):
    """Класс Cart реализует функционал корзины"""

    def __init__(self, request):
        """Инициализируем корзину"""

        self.session = request.session
        cart = self.session.get(settings.BASKET_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сеансе
            cart = self.session[settings.BASKET_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_pk: int, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """

        product_id = str(product_pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.BASKET_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product_pk: int) -> None:
        """Удаление товара (всей позиции) из корзины."""

        product_id = str(product_pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def products_cut_count(self, product_pk: int) -> None:
        """Удаление одного товара."""

        product_id = str(product_pk)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= 1
            self.save()

    def products_quantity(self, product_pk: int) -> int:
        """Получение кол-ва товаров."""

        product_id = str(product_pk)
        if product_id in self.cart:
            return self.cart[product_id]["quantity"]

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных."""

        for item in self.cart:

            yield {
                "pk_product": item,
                "quantity": self.cart[item]["quantity"],
            }

    def __len__(self):
        """Подсчет всех товаров в корзине."""

        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """Удаление корзины из сессии"""

        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True

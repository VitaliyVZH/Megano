
from _decimal import Decimal
from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.basket import Cart
from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderDetailsSerializer
from product.models import Product


class OrderView(APIView):
    """OrderView отдаёт данные о заказе и создаёт новый заказ"""

    def post(self, request, *args, **kwargs) -> Response:

        # получаем корзину пользователя
        cart = Cart(request)

        total_cost = sum([Decimal(product["price"]) for product in request.data])

        order = Order.objects.create(profile=request.user.profile, totalCost=total_cost)

        order_items = OrderItem.objects.all()
        for item in request.data:
            product = Product.objects.get(pk=item["id"])
            order_items.create(
                order=order,
                product=product,
                price=product.price * item["count"],
                quantity=item["count"]
            )

        cart.clear()
        return Response({"orderId": order.pk}, status=status.HTTP_200_OK)


class OrderDetailsView(APIView):
    """Класс обрабатывает детали заказа"""

    def get(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        serializer = OrderDetailsSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response:
        return Response(request.data, status=status.HTTP_200_OK)

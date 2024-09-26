
from rest_framework import serializers

from order.models import OrderItem, Order
from product.models import Product
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["pk", "order", "product", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор обрабатывает данные модели Order."""

    products = OrderItemSerializer(many=True, source="products_in_order")
    fullName = serializers.CharField(source="profile.fullName", read_only=True)
    email = serializers.CharField(source="profile.email", read_only=True)
    phone = serializers.CharField(source="profile.phone", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "createdAt", "fullName", "email", "phone", "deliveryType", "paymentType", "totalCost",
                  "status", "city", "address", "products"]

    def get_products(self, obj: Order):
        return [
            {
                "id": product.product.id,
                "title": product.product.title,
                "price": product.price,
                "count": product.quantity,
            }
            for product in obj.products_in_order.all()
        ]


class OrderDetailsSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)
    products = serializers.ModelSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'totalCost',
                  'status', 'city', 'address', 'products')

    def to_representation(self, instance: Order):
        def changing_quantity_goods_order(order_product: Product, quantity: int):
            order_product.count = quantity

            return order_product

        product = [
            changing_quantity_goods_order(
                order_product=values.product,
                quantity=values.quantity)
            for values in instance.products_in_order.all()
        ]
        products_serializer = ProductSerializer(product, many=True)

        data = {
            "pk": instance.pk,
            "createdAt": instance.createdAt,
            "fullName": instance.profile.fullName,
            "email": instance.profile.email,
            "phone": instance.profile.phone,
            "deliveryType": instance.deliveryType,
            "paymentType": instance.paymentType,
            "totalCost": instance.totalCost,
            "status": instance.status,
            "city": instance.city,
            "address": instance.address,
            "products": products_serializer.data
        }

        return data

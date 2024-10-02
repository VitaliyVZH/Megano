
from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки данных банковской карты пользователя"""

    class Meta:
        model = Payment
        fields = ["name", "code", "year", "number"]

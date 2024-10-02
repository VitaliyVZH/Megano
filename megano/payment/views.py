from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.serializers import PaymentSerializer


class PaymentAPIView(APIView):
    """Обработка данных со страницы получения заказов."""

    def post(self, request, *args, **kwargs) -> Response:
        """Обработка входящих данных с POST запроса с PaymentAPIView."""

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

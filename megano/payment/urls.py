from django.urls import path

from payment.views import PaymentAPIView

app_name = "payment"


urlpatterns = [
    path("payment", PaymentAPIView.as_view(), name="payment-detail"),
]

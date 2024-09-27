from django.urls import path

from payment.views import PaymentView

app_name = "payment"


urlpatterns = [
    path("payment", PaymentView.as_view(), name="payment-detail"),
    path("payment/<int:id>", PaymentView.as_view(), name="payment-detail"),
]

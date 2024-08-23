from django.urls import path

from sale.views import ProductSaleListAPIView

app_name = "sale"


urlpatterns = [
    path("sales/", ProductSaleListAPIView.as_view()),
]

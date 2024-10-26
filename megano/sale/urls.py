from django.urls import path
from django.views.decorators.cache import cache_page

from sale.views import ProductSaleListAPIView

app_name = "sale"


urlpatterns = [
    path("sales/", cache_page(60)(ProductSaleListAPIView.as_view()), name="sale"),
]

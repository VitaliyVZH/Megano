from django.urls import path

from sale.views import SaleAPIView

app_name = "sale"


urlpatterns = [
    path("sale/", SaleAPIView.as_view()),

]

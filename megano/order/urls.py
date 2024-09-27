from django.urls import path

from order.views import OrderView, OrderDetailsView

app_name = "order"


urlpatterns = [
    path("orders", OrderView.as_view(), name="order"),
    path("order/<int:pk>", OrderDetailsView.as_view()),
    path("orders/<int:pk>", OrderDetailsView.as_view()),
]

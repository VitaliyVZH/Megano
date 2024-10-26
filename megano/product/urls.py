from django.urls import path
from django.views.decorators.cache import cache_page

from product.views import TagsListAPIView, ProductDetailAPIView, ReviewProductAPIView

app_name = "product"


urlpatterns = [
    path("product/<int:pk>/", cache_page(60)(ProductDetailAPIView.as_view()), name="product_details"),
    path("product/<int:pk>/reviews", ReviewProductAPIView.as_view(), name="product_reviews"),
    path("tags/", cache_page(60)(TagsListAPIView.as_view()), name="product_tags"),
]

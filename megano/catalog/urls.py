from django.urls import path

from catalog.views import CatalogAPIView, CategoriesAPIView, ProductsPopularListAPIView, ProductsLimitedListAPIView, \
    BannersListAPIView, SalesListAPIView
from product.views import ProductAPIView

app_name = "catalog"


urlpatterns = [
    path("catalog/", CatalogAPIView.as_view()),
    path("categories/", CategoriesAPIView.as_view()),
    path("products/popular/", ProductsPopularListAPIView.as_view()),
    path("products/limited/", ProductsLimitedListAPIView.as_view()),
    # path("sales/", SalesListAPIView.as_view()),
    path("banners/", BannersListAPIView.as_view()),
]

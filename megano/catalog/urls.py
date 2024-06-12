from django.urls import path

from catalog.views import CatalogListAPIView, CategoriesAPIView, ProductsPopularListAPIView, ProductsLimitedListAPIView, \
    BannersListAPIView

app_name = "catalog"


urlpatterns = [
    path("catalog/", CatalogListAPIView.as_view()),
    path("categories/", CategoriesAPIView.as_view()),
    path("products/popular/", ProductsPopularListAPIView.as_view()),
    path("products/limited/", ProductsLimitedListAPIView.as_view()),
    # path("sales/", SalesListAPIView.as_view()),
    path("banners/", BannersListAPIView.as_view()),
]

from django.urls import path
from django.views.decorators.cache import cache_page  # декоратор кэширования

from catalog.views import CatalogListAPIView, CategoriesAPIView, ProductsPopularListAPIView, \
    ProductsLimitedListAPIView, BannersListAPIView

app_name = "catalog"


urlpatterns = [
    path("catalog/", cache_page(50)(CatalogListAPIView.as_view()), name="catalog-list"),
    path("categories/", cache_page(50)(CategoriesAPIView.as_view())),
    path("products/popular/", cache_page(50)(ProductsPopularListAPIView.as_view())),
    path("products/limited/", cache_page(50)(ProductsLimitedListAPIView.as_view())),
    path("banners/", cache_page(50)(BannersListAPIView.as_view())),
]

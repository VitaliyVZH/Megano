from django.urls import path

from catalog.views import CatalogAPIView, CategoriesAPIView
from product.views import ProductAPIView

app_name = "catalog"


urlpatterns = [
    path("catalog/", CatalogAPIView.as_view()),
    path("categories/", CategoriesAPIView.as_view()),
]

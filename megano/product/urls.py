from django.urls import path


from product.views import ProductAPIView, TagsListAPIView, ProductsDetailAPIView

app_name = "product"


urlpatterns = [
    path("product/", ProductAPIView.as_view()),
    path("product/<int:pk>/", ProductsDetailAPIView.as_view()),
    path("tags/", TagsListAPIView.as_view()),
]

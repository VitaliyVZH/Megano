from django.urls import path


from product.views import ProductAPIView, TagsListAPIView, ProductDetailAPIView

app_name = "product"


urlpatterns = [
    path("product/", ProductAPIView.as_view()),
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
    # path("product/<int:pk>/review/", ReviewProductAPIView.as_view()),
    path("tags/", TagsListAPIView.as_view()),
]

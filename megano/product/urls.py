from django.urls import path


from product.views import TagsListAPIView, ProductDetailAPIView, ReviewProductAPIView

app_name = "product"


urlpatterns = [
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
    path("product/<int:pk>/reviews", ReviewProductAPIView.as_view()),
    path("tags/", TagsListAPIView.as_view()),
]

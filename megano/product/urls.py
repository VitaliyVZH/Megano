from django.urls import path


from product.views import ProductAPIView, TagsListAPIView

app_name = "product"


urlpatterns = [
    path("product/", ProductAPIView.as_view()),
    path("tags/", TagsListAPIView.as_view()),
]

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from product.models import Category, Tag
from product.serializers import ProductSerializer, TagSerializer


class ProductAPIView(APIView):

    def get(self, request: Request) -> Response:
        serializer = ProductSerializer(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagsListAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

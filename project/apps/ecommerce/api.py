from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from ecommerce.models import Product
from ecommerce.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ['name']

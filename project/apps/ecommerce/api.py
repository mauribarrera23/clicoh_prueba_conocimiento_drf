from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from ecommerce.models import Product, OrderDetail, Order
from ecommerce.serializers import ProductSerializer, OrderDetailSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ['name']
    permission_classes = (IsAuthenticated,)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['product__name']
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        order_detail = OrderDetail.objects.filter(order=serializer.validated_data['order'],
                                                  product=serializer.validated_data['product'].id)
        if order_detail.exists():
            raise ValidationError("El producto ya se encuentra seleccionado en la orden.")
        if quantity > product.stock or quantity <= 0:
            raise ValidationError(f"Producto sin stock. Stock disponible: {product.stock} unidades.")
        product.stock = product.stock - serializer.validated_data['quantity']
        product.save()
        return serializer.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        product = instance.product
        if serializer.validated_data['quantity'] > product.stock or serializer.validated_data['quantity'] <= 0:
            raise ValidationError(f"Producto sin stock. Stock disponible: {product.stock} unidades.")
        if instance.quantity < serializer.validated_data['quantity']:
            product.stock = product.stock - (serializer.validated_data['quantity'] - instance.quantity)
            product.save()
        if instance.quantity > serializer.validated_data['quantity']:
            product.stock = product.stock + (instance.quantity - serializer.validated_data['quantity'])
            product.save()
        return serializer.save()

    def perform_destroy(self, instance):
        product = instance.product
        product.stock = product.stock + instance.quantity
        product.save()
        return instance.delete()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('order_detail', 'order_detail__product')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        for detail in instance.order_detail.all():
            product = detail.product
            product.stock = product.stock + detail.quantity
            product.save()
        return instance.delete()

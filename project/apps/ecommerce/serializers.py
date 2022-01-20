from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from ecommerce.models import Product, OrderDetail, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

    included_serializers = {
        'product': ProductSerializer
    }

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Debe seleccionar al menos un producto.")
        if data['quantity'] > data['product'].stock or data['quantity'] <= 0:
            raise serializers.ValidationError(
                f"Producto sin stock. Stock disponible: {data['product'].stock} unidades.")
        return data


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(method_name='get_total')

    class Meta:
        model = Order
        fields = ('date_time', 'order_detail', 'total')
        extra_kwargs = {
            'order_detail': {'required': False},
        }

    included_serializers = {
        'order_detail': OrderDetailSerializer,
    }

    def get_total(self, order):
        total = 0
        for detail in order.order_detail.all():
            total = total + detail.product.price * detail.quantity
        return total

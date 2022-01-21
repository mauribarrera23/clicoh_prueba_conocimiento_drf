from rest_framework_json_api import serializers
from ecommerce.models import Product, OrderDetail, Order
from ecommerce.utils import get_dolar_blue


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
        return data


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(method_name='get_total')
    total_usd = serializers.SerializerMethodField(method_name='get_total_usd')

    class Meta:
        model = Order
        fields = ('date_time', 'order_detail', 'total', 'total_usd')
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

    def get_total_usd(self,order):
        total_usd = get_dolar_blue(self.get_total(order))
        return round(total_usd, 2)

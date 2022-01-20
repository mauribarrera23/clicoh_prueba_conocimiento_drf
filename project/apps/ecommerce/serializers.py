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
            raise serializers.ValidationError(f"Producto sin stock. Stock disponible: {data['product'].stock} unidades.")
        return data

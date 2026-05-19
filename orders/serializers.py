from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Cart

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'product_price', 
                  'variant_name', 'quantity', 'subtotal')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'status', 'payment_status', 
                  'shipping_address', 'shipping_city', 'shipping_state', 
                  'shipping_country', 'shipping_pincode', 'subtotal', 
                  'shipping_charge', 'discount', 'tax', 'total', 
                  'payment_method', 'notes', 'items', 'created_at')
        read_only_fields = ('order_number', 'status', 'payment_status', 'created_at')

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField()
    shipping_state = serializers.CharField()
    shipping_country = serializers.CharField()
    shipping_pincode = serializers.CharField()
    payment_method = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
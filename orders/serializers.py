from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'product', 'payment_id', 'order_date', 'total_cost', 'quantity', 'created_at', 'updated_at']
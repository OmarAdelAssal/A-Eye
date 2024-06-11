from rest_framework import serializers
from .models import Payment
from customers.serializers import CustomerSerializer  # Assuming you have a CustomerSerializer defined

class PaymentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()  # Assuming CustomerSerializer is defined

    class Meta:
        model = Payment
        fields = ['id', 'customer', 'payment_method', 'payment_date']
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import CartItem, Product, Cart


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Use PrimaryKeyRelatedField for write operations

    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        product = validated_data.pop('product')
        cart = validated_data.pop('cart')
        quantity = validated_data.pop('quantity')
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def create(self, validated_data):
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(customer=self.context['request'].user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set')

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'items']
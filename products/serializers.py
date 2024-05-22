from rest_framework import serializers

from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryName']

class ProductSerializer(serializers.ModelSerializer):
    # Nested serializer to include category details
    category = CategorySerializer()  

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'price', 'category']
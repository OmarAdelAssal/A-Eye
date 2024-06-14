from rest_framework import serializers

from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryName', 'categoryLogo']

class ProductSerializer(serializers.ModelSerializer):
    # Nested serializer to include category details
    category = CategorySerializer()  

    class Meta:
        model = Product
        # fields = ['id', 'name', 'quantity', 'price','product_image', 'category']
        fields = '__all__'
from rest_framework import serializers

from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryName', 'categoryLogo']

    def get_categoryLogo(self, obj):
        request = self.context.get('request')
        if obj.categoryLogo and request:
            return request.build_absolute_uri(obj.categoryLogo.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    # Nested serializer to include category details
    category = CategorySerializer()  

    class Meta:
        model = Product
        # fields = ['id', 'name', 'quantity', 'price','product_image', 'category']
        fields = '__all__'

    def get_product_image(self, obj):
        request = self.context.get('request')
        if obj.product_image and request:
            return request.build_absolute_uri(obj.product_image.url)
        return None    
from rest_framework import viewsets , filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product 
# @action decorator to create a custom action named retrieve_product
from rest_framework.decorators import action
from .serializers import CategorySerializer, ProductSerializer

# Class for Category model to create and retrive category
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class to create and retrive all products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'category__categoryName']

    def create(self, request, *args, **kwargs):
        category_name = request.data.get('category.categoryName')  # Get category name from request data
        if not category_name:
            return Response({'error': 'Category name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(categoryName=category_name)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)  # Associate product with existing category
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        category_name = request.data.get('category.categoryName')  # Get category name from request data
        if not category_name:
            return Response({'error': 'Category name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(categoryName=category_name)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)  # Associate product with existing category
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # @action decorator to create a custom action named retrieve_product
    # The retrieve_product action is mapped to the GET method and is designed to retrieve a single product by its ID (pk).
    @action(detail=True, methods=['get'])
    def retrieve_product(self, request, pk=None):
        try:
            product = self.get_object()
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

# The following class is to return all products in specific category
class ProductsInCategoryAPIView(APIView):
    def get(self, request, category_id):
        try:
            products = Product.objects.filter(category__id=category_id)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
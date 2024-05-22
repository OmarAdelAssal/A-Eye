from rest_framework import viewsets, permissions , status
from rest_framework.authentication import TokenAuthentication
from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response

# class IsCustomer(permissions.BasePermission):
#     """
#     Custom permission to only allow customers to create orders.
#     """
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if hasattr(request.user, 'customer'):
#                 return True
#         return False

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        if product.quantity < 1:
            return Response({'detail': 'Product is out of stock.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Decrease the product quantity
        product.quantity -= 1
        product.save()
        



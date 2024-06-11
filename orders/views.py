'''

from rest_framework import viewsets, permissions , status
from rest_framework.authentication import TokenAuthentication
from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

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
        quantity = serializer.validated_data['quantity']
        
        if product.quantity < quantity:
            raise ValidationError('Product is out of stock.')
        
        # Calculate the total cost
        total_cost = product.price * quantity

        # Decrease the product quantity
        product.quantity -= quantity
        product.save()
        serializer.save(total_cost=total_cost)
'''
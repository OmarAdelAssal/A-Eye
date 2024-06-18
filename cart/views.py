from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, F, DecimalField
from django.shortcuts import get_object_or_404
from cart.serializers import CartSerializer, AddToCartSerializer,CartItemSerializer
from cart.models import CartItem,Cart
from customers.models import Customer
from products.models import Product
import jwt, datetime

class CartItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        customer = Customer.objects.filter(id=payload['id']).first()
        if not customer:
            raise AuthenticationFailed("Customer not found!")

        cart = get_object_or_404(Cart, customer=customer)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    


class AddToCartAPIView(APIView):
    serializer_class = AddToCartSerializer

    def post(self, request):
        # Get the JWT token from the cookies
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the token to get the user ID
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Get the customer based on the payload ID
        customer = get_object_or_404(Customer, id=payload['id'])

        # Get the cart associated with the customer
        cart, created = Cart.objects.get_or_create(customer=customer)

        # Serialize and validate the incoming data
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            # Check product availability
            product = get_object_or_404(Product, id=product_id)
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()
            else:
                return Response({'error': 'Insufficient quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

            # Create or update the cart item
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

            return Response({'status': 'Item added to cart'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveFromCartAPIView(APIView):
    def delete(self, request, product_id):
        # Get the JWT token from the cookies
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the token to get the user ID
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Get the customer based on the payload ID
        customer = get_object_or_404(Customer, id=payload['id'])

        # Get the cart associated with the customer
        cart = get_object_or_404(Cart, customer=customer)

        # Get the cart item to be removed
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        # Restore the product quantity
        product = cart_item.product
        product.quantity += cart_item.quantity
        product.save()

        # Delete the cart item
        cart_item.delete()

        return Response({'status': 'Item removed from cart'}, status=status.HTTP_200_OK)

class ClearCartAPIView(APIView):
    def delete(self, request):
        # Get the JWT token from the cookies
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the token to get the user ID
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Get the customer based on the payload ID
        customer = get_object_or_404(Customer, id=payload['id'])

        # Get the cart associated with the customer
        cart = get_object_or_404(Cart, customer=customer)

        # Get all cart items and restore the product quantities
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            product = cart_item.product
            product.quantity += cart_item.quantity
            product.save()
            cart_item.delete()

        return Response({'status': 'Cart cleared'}, status=status.HTTP_200_OK)

class CartItemListAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the JWT token from the cookies
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the token to get the user ID
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Get the customer based on the payload ID
        customer = get_object_or_404(Customer, id=payload['id'])

        # Get the cart associated with the logged-in customer
        cart = get_object_or_404(Cart, customer=customer)

        # Filter CartItems by the retrieved cart
        queryset = CartItem.objects.filter(cart=cart)
        return queryset

    def get_total_cost(self, queryset):
        total_cost = queryset.annotate(
            total_price=F('product__price') * F('quantity')
        ).aggregate(total_cost=Sum('total_price', output_field=DecimalField()))['total_cost']
        return total_cost

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_cost = self.get_total_cost(queryset)
        serializer = self.serializer_class(queryset, many=True)
        
        for item in serializer.data:
            item['product_price'] = CartItem.objects.get(id=item['id']).product.price
        
        data = {
            'total_cost': total_cost,
            'cart_items': serializer.data
        }
        return Response(data)
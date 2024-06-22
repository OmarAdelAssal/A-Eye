from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from customers.models import Customer
from products.models import Product
from .models import Order, OrderItem,Cart, CartItem
from .serializers import OrderSerializer
import jwt

class CheckoutAPIView(APIView):
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
        cart = get_object_or_404(Cart, customer=customer)

        # Check if the cart is empty
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = Order.objects.create(customer=customer, total_cost=0)

        total_cost = 0

        # Transfer cart items to order items
        for cart_item in cart_items:
            product = cart_item.product
            if product.quantity < cart_item.quantity:
                return Response({'error': f'Insufficient quantity for product {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
            
            product.quantity -= cart_item.quantity
            product.save()

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price * cart_item.quantity
            )

            total_cost += order_item.price
            cart_item.delete()

        # Update total cost of the order
        order.total_cost = total_cost
        order.save()

        # Serialize the order
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderHistoryAPIView(APIView):
    def get(self, request):
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

        # Get all orders for the customer
        orders = Order.objects.filter(customer=customer).order_by('-created_at')

        # Serialize the orders
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    '''
    class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        customer = Customer.objects.get(id=payload['id'])
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_cost = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(customer=customer, total_cost=total_cost)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

        cart_items.delete()

        payment_data = {
            'customer': customer.id,
            'order': order.id,
            'payment_method': request.data.get('payment_method', 'COD'),
            'amount': total_cost,
        }
        payment_serializer = PaymentSerializer(data=payment_data)
        if payment_serializer.is_valid():
            payment_serializer.save()

        return Response({"message": "Order placed and payment recorded successfully"}, status=status.HTTP_201_CREATED)
    '''
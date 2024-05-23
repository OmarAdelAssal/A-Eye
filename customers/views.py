from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
import jwt, datetime
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

class SignUpView(viewsets.ModelViewSet):
    """
    Create a new Customer.
    """

    queryset = Customer.objects.none()
    serializer_class = CustomerSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        customer = Customer.objects.filter(email=email).first()

        if customer is None:
            raise AuthenticationFailed('Customer not found')
            
        if not customer.check_password(password):
            raise AuthenticationFailed('Invalid password')

        payload = {
            "id": customer.id,
            "email": customer.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response() 
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt token': token}

        return response

class CustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        customer = Customer.objects.filter(id=payload['id']).first()
        serializer = CustomerSerializer(customer)

        return Response(serializer.data)

class UpdateCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        customer = Customer.objects.filter(id=payload['id']).first()
        if customer is None:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        customer = Customer.objects.filter(id=payload['id']).first()
        if customer is None:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()

        return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'successful'}

        return response

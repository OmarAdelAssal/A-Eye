from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer

import jwt, datetime
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed


class SignUpView(viewsets.ModelViewSet):
    """
    Create a new Customer.
    """

    queryset = Customer.objects.none()
    serializer_class = CustomerSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        #find Customer using email
        customer = Customer.objects.filter(email=email).first()

        if customer is None:
            raise AuthenticationFailed('Customer not found:)')
            
        if not customer.check_password(password):
            raise AuthenticationFailed('Invalid password')

        payload = {
            "id": customer.id,
            "email": customer.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # token.decode('utf-8')
        #we set token via cookies
        

        response = Response() 

        response.set_cookie(key='jwt', value=token, httponly=True)  #httonly - frontend can't access cookie, only for backend

        response.data = {
            'jwt token': token
        }

        #if password correct
        return response
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successful'
        }

        return response
# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Customer
# from .serializers import CustomerSerializer
# # Create your views here.
# # class SignUpView(viewsets.ModelViewSet):
# #     """
# #     Create a new Customer.
# #     """

# #     queryset = Customer.objects.none()
# #     serializer_class = CustomerSerializer

# #     def create(self, request):
# #         serializer = self.serializer_class(data=request.data)
# #         # serializer.is_valid(raise_exception=True)
# #         serializer.is_valid()
# #         serializer.save()
# #         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SignUpView(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 
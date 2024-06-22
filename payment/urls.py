from django.urls import path
from .views import CreatePaymentAPIView, ListPaymentsAPIView

urlpatterns = [
    path('create/', CreatePaymentAPIView.as_view(), name='create-payment'),
    path('list/', ListPaymentsAPIView.as_view(), name='list-payments'),
]
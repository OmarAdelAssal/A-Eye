from django.urls import path, include
from .views import CheckoutAPIView, OrderHistoryAPIView
urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('history/', OrderHistoryAPIView.as_view(), name='order-history'),
]
'''

from rest_framework.routers import DefaultRouter
from .views import OrderView

router = DefaultRouter()
router.register(r'', OrderView)
'''
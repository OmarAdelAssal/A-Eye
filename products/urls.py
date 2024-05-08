from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # retrive product alone based on id
    path('<int:pk>/', ProductViewSet.as_view({'get': 'retrieve_product'}), name='product-detail'),
    
    
]
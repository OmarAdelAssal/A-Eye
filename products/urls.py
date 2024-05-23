from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # retrive product alone based on id
    path('<int:pk>/', ProductViewSet.as_view({'get': 'retrieve_product'}), name='product-detail'),
    
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
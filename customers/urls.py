from django.urls import path, include
from customers.views import SignUpView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', SignUpView)



urlpatterns = [
    path('signup/', include(router.urls)),

]



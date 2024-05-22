from django.urls import path, include
from customers.views import SignUpView, LoginView, LogoutView, CustomerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', SignUpView)

router2 = DefaultRouter()
# router2.register('', CustomerViewSet)

urlpatterns = [
    path('signup/', include(router.urls)),
    # path("login/", LoginView.as_view({"post": "login"})),
    # path('login/', include(router2.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("<int:pk>/", CustomerViewSetas_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # path("<int:pk>/",include(router2.urls))
    path("customer/", CustomerView.as_view())
]



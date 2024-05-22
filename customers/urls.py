from django.urls import path, include
from customers.views import SignUpView, LoginView, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', SignUpView)

router2 = DefaultRouter()
# router2.register('', LoginView)

urlpatterns = [
    path('signup/', include(router.urls)),
    # path("login/", LoginView.as_view({"post": "login"})),
    # path('login/', include(router2.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")

]



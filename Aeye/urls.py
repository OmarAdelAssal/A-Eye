"""
URL configuration for Aeye project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views import ProductsInCategoryAPIView, CategoryViewSet ,ProductViewSet
from cart.views import CartDetailAPIView, AddToCartAPIView, CartItemListAPIView, CartItemListCreateAPIView, RemoveFromCartAPIView, ClearCartAPIView

from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from customers.views import SignUpView
router = routers.DefaultRouter()
router.register(r'', CategoryViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include("customers.urls")),
    path('products/', include("products.urls")),
    path('orders/', include("orders.urls")),
    path('categories/<int:category_id>/products/',
        ProductsInCategoryAPIView.as_view(), name='products_in_category'),
    path('products/search/', ProductViewSet.as_view({'get': 'search'}), name='product-search'),
    # Categories Endpoints
    path('categories/', include(router.urls)),
    ######  Cart Endpoints  ######
    # Show the details of cart
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    # will comment next line and remove urls in cart.urls and put it all here
    # path('cart/', include('cart.urls')),
    # add items to cart
    path('add-to-cart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    # to return all items with prices and total cost in specefic cart with its id (NEED TO CHANGE IT)
    # path('cart/<int:cart_id>/items/', CartItemListAPIView.as_view(), name='cart-item-list'), # old one
    # the following api to remove product from cart 
    path('remove-from-cart/<int:product_id>/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    # Api to remove all items from cart
    path('cart/clear/', ClearCartAPIView.as_view(), name='clear-cart'),
    # list all items of cart with the total price
    path('cart/items/', CartItemListAPIView.as_view(), name='cart-item-list'),
    #### Api Documentation Urls ###
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
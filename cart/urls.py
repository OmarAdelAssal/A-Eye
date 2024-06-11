from django.urls import path, include
from cart.views import CartDetailAPIView, AddToCartAPIView, CartItemListAPIView, CartItemListCreateAPIView

urlpatterns = [
    path('', CartDetailAPIView.as_view(), name='cart-detail'),
    # Retrives all carts items to all users (NOT NECESSARY)
    path('cart-items/', CartItemListCreateAPIView.as_view(), name='cartitem-list-create'),
    # add items to cart
    path('add-to-cart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    # retrurn all items in specefic cart using cart id and calculate total cost of all cart items
    path('cart-items/<int:cart_id>/', CartItemListAPIView.as_view(), name='cart-item-list'),
    # to return all items with prices and total cost in specefic cart with its id (NEED TO CHANGE IT)
    path('cart/<int:cart_id>/items/', CartItemListAPIView.as_view(), name='cart-item-list'),
]
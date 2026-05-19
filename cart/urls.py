from django.urls import path
from .views import CartView, CartItemUpdateView, ClearCartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('item/<int:item_id>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('clear/', ClearCartView.as_view(), name='clear-cart'),
]
from django.urls import path
from . import views


app_name = 'outgoing'

urlpatterns = [
    path('cart', views.cart, name="cart"),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    # path('add_cart/<int:product_id>/increase/', views.add_cart, {'action': 'increase'}, name='add_cart_increase'),
    # Other URL patterns
]




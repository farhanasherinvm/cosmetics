from django.urls import path
from . import views


app_name = 'outgoing'

urlpatterns = [
    path('cart', views.cart, name="cart"),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/', views.remove_item, name='remove_item'),

    path('check_out', views.check_out, name="check_out"),
    # path('add_cart/<int:product_id>/increase/', views.add_cart, {'action': 'increase'}, name='add_cart_increase'),
    # Other URL patterns
]




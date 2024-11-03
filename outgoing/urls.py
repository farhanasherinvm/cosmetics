from django.urls import path
from . import views


app_name = 'outgoing'

urlpatterns = [
    path('cart', views.cart, name="cart"),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/', views.remove_item, name='remove_item'),

    path('checkout', views.checkout, name="checkout"),
    path('new_address', views.new_address, name="new_address"),
    path('delete_address/<int:id>/', views.delete_address, name="delete_address"),
    path('place_order', views.place_order, name="place_order"),
    path('paypal_payment', views.paypal_payment, name="paypal_payment"),
    path('paypal_redirect', views.paypal_redirect, name="paypal_redirect"),
    path('paypal_success', views.paypal_success, name="paypal_success"),
    path('paypal_cancel', views.paypal_cancel, name="paypal_cancel"),
    # path('cash_on_delivery/<int:number>/', views.cash_on_delivery, name="cash_on_delivery")
 
    # path('add_cart/<int:product_id>/increase/', views.add_cart, {'action': 'increase'}, name='add_cart_increase'),
   
]




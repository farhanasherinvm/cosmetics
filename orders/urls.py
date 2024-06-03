from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    # path('recieved_mail', views.order_success, name="order_success"),
    path('order_tracking', views.order_tracking, name="order_tracking"),
]
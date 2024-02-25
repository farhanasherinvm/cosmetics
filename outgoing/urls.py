from django.urls import path
from .  import views
app_name='outgoing'
urlpatterns = [
     path('cart',views.cart,name="cart")
  
   
]
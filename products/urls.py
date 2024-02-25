from django.urls import path
from .  import views
app_name='products'
urlpatterns = [
    
   path('category/<slug:category_slug>/<slug:product_slug>', views.single_product, name='single_product'),
   path('products', views.product, name="products"),
]
from django.urls import path
from .  import views
app_name = 'shop'
urlpatterns = [
   path('shop', views.shop, name='shop'),
   
   path('product', views.product, name="product"),
   path('<slug:category_slug>/', views.shop, name='products_by_category'),
   path('single_product/<slug:category_slug>/<slug:product_slug>/', views.single_product, name='single_product'),
]
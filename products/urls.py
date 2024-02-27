from django.urls import path
from .  import views
app_name = 'shop'
urlpatterns = [
   path('shop', views.shop, name='shop'),
   path('product/<str:slug>/<int:id>', views.product, name='product'),
   path('productlist', views.productlist, name="productlist"),
   # path('<slug:category_slug>/', views.shop, name='products_by_category'),
  
]
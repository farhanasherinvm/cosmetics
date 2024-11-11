from django.urls import path
from .  import views
#from .views import ajax_product_search
app_name = 'shop'
urlpatterns = [
   path('shop', views.shop, name='shop'),
   path('product/<str:slug>/<int:id>', views.product, name='product'),
   #path('productlist', views.productlist, name="productlist"),
   # path('<slug:category_slug>/', views.shop, name='products_by_category'),
     path('ajax-product-search/', views.ajax_product_search, name='ajax_product_search'),
  
]
from django.urls import path
from .  import views

app_name = 'adminpanel'
urlpatterns = [
    
    
    path('admlogin',views.admlogin,name="admlogin"),
    path('admlogout',views.admlogout,name="admlogout"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('users',views.users,name="users"),
    path('newuser',views.newuser,name="newuser"),


    path('category_manage',views.category_manage,name="category_manage"),
    path('add_category',views.add_category,name="add_category"),
    path('edit_category',views.edit_category,name="edit_category"),
    path('category_delete/<str:category_id>/',views.category_delete,name="category_delete"),
  
    path('product_manage/', views.product_manage, name='product_manage'),
    path('add_product',views.add_product,name="add_product"),
    path('product_list/<str:id>/',views.product_list,name="product_list"),
    path('edit_product',views.edit_product,name="edit_product")

]



from django.urls import path
from .  import views

urlpatterns = [
    
    path('',views.home,name="home"),
    path('login',views.userlogin,name="userlogin"),
    path('signup',views.usersignup,name="usersignup"),
    path('userlogout',views.userlogout,name="userlogout"),
    path('otp',views.user_otp,name="user_otp"),
 
]
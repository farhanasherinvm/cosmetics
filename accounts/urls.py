from django.urls import path
from .  import views


app_name = 'accounts'


urlpatterns = [
    
  
    path('otp',views.user_otp,name="otp"),
    path('usersignup',views.usersignup,name='usersignup'),
    path('userlogin',views.userlogin,name="userlogin"),
    path('userlogout',views.userlogout,name="userlogout"),
]
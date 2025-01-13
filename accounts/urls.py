from django.urls import path
from .  import views


app_name = 'accounts'


urlpatterns = [
    
    path('invoice',views.invoice,name="invoice"),
    path('otp',views.user_otp,name="otp"),
    path('new_otp',views.new_otp,name="new_otp"),
    path('usersignup',views.usersignup,name='usersignup'),
    path('userlogin',views.userlogin,name="userlogin"),
    path('userlogout',views.userlogout,name="userlogout"),
    path('profile',views.profile,name="profile"),
    path('edit_profile',views.edit_profile,name="edit_profile"),
]
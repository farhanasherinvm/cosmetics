from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(null=True,blank=True)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15,default=True,null=True)
    country = models.CharField(max_length=15)
    image = models.ImageField( upload_to='images/',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    wallet= models.DecimalField(default=0, decimal_places=2, max_digits=10, null=True, blank=True) 

    def __str__(self):
        print(f"User instancessssssssss: {self.user}")
        return self.user.username

    def user_name(self):
        print(f"User first_name: {self.user.first_name}")
        print(f"User last_name: {self.user.last_name}")
        return f"{self.user.first_name} {self.user.last_name}"
    

class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    new_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    phone=models.BigIntegerField(max_length=15)
    address=models.TextField(max_length=20)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50) 
    country=models.CharField(max_length=50)
    zip=models.BigIntegerField(max_length=6, default='00000')
    def __str__(self):
        return self.user.username
    
class Wallet(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=True, blank=True)
    transaction    = models.CharField(max_length=150, blank=True, null=True)
    amount         = models.CharField(max_length=100)
    created_at     = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"PaymentWallet for User: {self.user}, Created on: {self.created_at}"
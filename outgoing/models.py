from django.db import models
from products.models import Product
from django.contrib.auth.models import User
# Create your models here.
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return self.user
class Cart(models.Model):
    cart_id    = models.CharField(max_length=250 , blank=True)
    added_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id
    
class Cartitem(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity  = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity


    def __str__(self):
        return self.product.product_name
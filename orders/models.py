import datetime
import uuid
from django.db import models
from accounts.models import User_Profile
from products.models import Product
# Create your models here.

class Payment(models.Model):
    user       = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    method     = models.CharField(max_length=100)
    amount     = models.CharField(max_length=100)
    status     = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.method
    

    
class Order(models.Model):

    ORDER_STATUS = (
        (1, 'New'),
        (2, 'Accepted'),
        (3, 'Preparing'),
        (4, 'On Shipping'),
        (5, 'Completed'),
        (6, 'Cancelled'),
        (7, 'Return')
    )
    order_number = models.CharField(max_length=50, unique=True)
    user         = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    payment      = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True,null=True)
    user_name    = models.CharField(max_length=50)
    address      = models.CharField(max_length=100)
    email        = models.EmailField(max_length=50)
    phone        = models.CharField(max_length=15)
    city         = models.CharField(max_length=50)
    state        = models.CharField(max_length=50)
    country      = models.CharField(max_length=50)
    zip          = models.BigIntegerField(max_length=6, default='00000')
    status       = models.IntegerField(choices=ORDER_STATUS, default=1, null=True, blank=True)
    ip           = models.CharField(blank=True, max_length=20)
    is_ordered   = models.BooleanField(default=False)
    order_total  = models.FloatField(default=0.0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            today = datetime.today()
            date_str = today.strftime('%Y%m%d')
            unique_str = str(uuid.uuid4()).replace('-', '').upper()[:3]
            self.order_number = f"{date_str}-{unique_str}"
        super().save(*args, **kwargs)


class OrderProduct(models.Model):
    STATUS = (
        ('New' , 'New'),
        ('Accepted' , 'Accepted'),
        ('Return' , 'Return'),
        ('Cancelled' , 'Cancelled'),
    )
    user       = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    order      = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment    = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    image      = models.ImageField(upload_to='photos/products')
    product    = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity   = models.IntegerField()
    price      = models.FloatField()
    ordered    = models.BooleanField(default=False)
    status     = models.CharField(choices=STATUS, default="New")
    ip         = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_note  = models.CharField(blank=True,max_length=100)

    def __str__(self):
        return self.product.product_name
    def subtotal(self):
        return self.price * self.quantity



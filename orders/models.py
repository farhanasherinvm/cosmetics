from django.db import models
from accounts.models import User_Profile
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

    user         = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    payment      = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    user_name    = models.CharField(max_length=50)
    address      = models.CharField(max_length=100)
    email        = models.EmailField(max_length=50)
    phone        = models.CharField(max_length=15)
    city         = models.CharField(max_length=50)
    state        = models.CharField(max_length=50)
    country      = models.CharField(max_length=50)
    status       = models.IntegerField(choices=ORDER_STATUS, default=1, null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
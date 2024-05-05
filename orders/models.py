from django.db import models
from accounts.models import User_Profile
# Create your models here.

class Payment(models.Model):
    user      = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    payment_id= models.CharField(max_length=100)
    method    = models.CharField(max_length=100)
    amount    = models.CharField(max_length=100)
    status    = models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.method
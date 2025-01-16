from outgoing.models import Wishlist
from products.models import Category, Product
# Create your views here.

from django.shortcuts import render, redirect





def home(request):
    
    product=Product.objects.all()
    category=Category.objects.all()
    wishlist_items=Wishlist.objects.filter(user=request.user)
    context={
        'product':product,
        'category':category,
        'wishlist_items':wishlist_items
    }
    return render(request,"home.html",context)

from outgoing.models import Wishlist
from products.models import Category, Product
# Create your views here.

from django.shortcuts import render, redirect





def home(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        wishlist_items = [] 
    product=Product.objects.all()
    category=Category.objects.all()
        
    context={
        'product':product,
        'category':category,
        'wishlist_items':wishlist_items
        }
    return render(request,"home.html",context)

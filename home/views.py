from products.models import Category, Product
# Create your views here.

from django.shortcuts import render, redirect





def home(request):
    
    product=Product.objects.all()
    category=Category.objects.all()

    context={
        'product':product,
        'category':category,
    }
    return render(request,"home.html",context)

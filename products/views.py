
from django.shortcuts import get_object_or_404, render
from .models import Product

# Create your views here.
def product(request):
    return render(request,"productlist.html")



def single_product(request,category_slug,product_slug):
    print("haaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    try:    
        single_product =Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context={
      
        'single_product':single_product,
   }
    
    return render(request,'productlist.html', context)
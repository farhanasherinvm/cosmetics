
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category
from .models import Product

# Create your views here.
def product(request,slug,id):
    print("haaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(f'product id is :{id}')
    product = Product.objects.get(id=id)
    return render(request, 'productlist.html', {'data':product})
   
def productlist(request):
    return render (request,'productlist.html')
from django.http import JsonResponse
from .models import Product

def ajax_product_search(request):
    query = request.GET.get('query', '')
    if query:
        products = Product.objects.filter(product_name__icontains=query)[:5]  # Use 'product_name' here
        product_list = [
            {
                'name': product.product_name,
                'price': product.price,
                'image': product.image.url if product.image else None,
            }
            for product in products
        ]
        return JsonResponse({'products': product_list})
    return JsonResponse({'products': []})

# def single_product(request,category_slug,product_slug):
#     print("haaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#     try:    
#         single_product =Product.objects.get(category__slug=category_slug, slug=product_slug)
#     except Exception as e:
#         raise e
#     context={
      
#         'single_product':single_product,
#    }
    
#     return render(request,'productlist.html', context)

def shop(request):
    product=Product.objects.all()
    category=Category.objects.all()
    
    context={
        'product':product,
        'category':category
    }
    return render(request, 'shop.html', context)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from outgoing.models import Wishlist
from .models import Category
from .models import Product

# Create your views here.
def product(request,slug,id):
    print("haaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(f'product id is :{id}')
   
    product = Product.objects.get(id=id)
    variants=product.variants.all()
    print("variants",variants)
    context={
        'product':product,
        'variants':variants
    }
    print(f"Number of variants: {variants.count()}")
    for var in product.variants.all():
        print(var.image.url)  # Check if each variant has an image

    return render(request, 'productlist.html',context)
   
# def productlist(request):
#     return render (request,'productlist.html')


def ajax_product_search(request):
    query = request.GET.get('query', '')
    if query:
        products = Product.objects.filter(product_name__icontains=query)[:5]  # Use 'product_name' here
        product_list = [
            {
                'name': product.product_name,
                'price': product.price,
                'image': product.image.url if product.image else None,
                'url': reverse('shop:product', kwargs={'slug': product.slug, 'id': product.id})  # Generate product detail URL
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

def add_wishlist(request,product_id):
    product=get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user,product=product)
    return redirect(request.META.get('HTTP_REFERER', '/'))
# def filter(request):
#     price_range = request.GET.get('price_range')  # e.g., "0;5000"
#     categories = request.GET.getlist('category')  # e.g., ["nail", "makeup"]
#     products = Product.objects.filter(is_available=True)  # Start with all available products

#     # Handle price range filter
#     if price_range:
#         try:
#             min_price, max_price = map(float, price_range.split(';'))
#             products = products.filter(price__gte=min_price, price__lte=max_price)
#         except ValueError:
#             return render(request, 'shop.html', {
#                 'products': products,
#                 'error_message': 'Invalid price range format.'
#             })

#     # Handle category filter
#     if categories:
#         # Assuming `Category` model has a `category_name` field
#         products = products.filter(category__category_name__in=categories)

#     return render(request, 'shop.html', {'products': products})

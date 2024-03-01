from django.http import HttpResponse
from django.shortcuts import redirect, render
from outgoing.models import Cart , Cartitem
from products.models import Product

# Create your views here.
def cart(request):
    return render(request,"cart.html")

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart= request.session.create()
    return cart

def add_cart(request,product_id):
    print("kuuui")
    product = Product.objects.get(id=product_id)#get product
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))# get the cart using cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id= _cart_id(request)
        ) 
    cart.save()

    try:
        cart_item =Cartitem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart = cart.save()
    return HttpResponse(cart_item.quantity)   
    return redirect('outgoing:cart')
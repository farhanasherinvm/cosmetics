from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from outgoing.models import Cart , Cartitem
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def cart(request, total=0, quantity=0, cart_item=None):
    try:
        print("11111111111")
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            print("222222")
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            print("suuuuuuuuuuuuuuuuuuuuuuuuuuuuuiiiiiiii")
    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
    }
    print(f'item:{cart_items}')
    print(f'total:{quantity}')
    print(f'total:{total}')

    return render(request,"cart.html", context)

def _cart_id(request):
    
    cart = request.session.session_key
    print("33333333333")
    if not cart:
        print("44444444444")
        cart= request.session.create()
    return cart

def add_cart(request,product_id):
    print("kuuui")
    product = Product.objects.get(id=product_id)#get product
    try:
        print("555")
        cart=Cart.objects.get(cart_id=_cart_id(request))# get the cart using cart_id present in the session
    except Cart.DoesNotExist:
        print("666666")
        cart = Cart.objects.create(
            cart_id= _cart_id(request)
        ) 
    cart.save()
    print("7777")
    try:
        print("88888888")
        cart_item =Cartitem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        print("999999999")
        cart_item = Cartitem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart = cart.save()
    #return HttpResponse(cart_item.quantity)   
    return redirect('outgoing:cart')



# def update_quantity(request, product_id, action):
#     # Assume you have a Cart model and 'quantity' field
#     # Replace this with your actual model and field names
#     cart_item = Cart.objects.get(id=product_id)

#     if action == 'increase':
#         cart_item.quantity += 1
#     elif action == 'decrease' and cart_item.quantity > 1:
#         cart_item.quantity -= 1

#     cart_item.save()

#     # Return the updated quantity in JSON format
#     return JsonResponse({'quantity': cart_item.quantity})
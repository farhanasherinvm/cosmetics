import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from outgoing.models import Cart , Cartitem
from products.models import Product 
from orders.models import Order
from accounts.models import User_Profile ,Address
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Create your views here.
def cart(request, total=0, quantity=0, cart_item=None):

    cart_items = []  # Initialize cart_items as an empty list
    tax = 0  # Initialize tax
    grand_total = 0  # Initialize grand_total
    

    try:
        print("11111111111")
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            print("222222")
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax= ( 2 * total)/100
        grand_total = tax + total    
        print("suuuuuuuuuuuuuuuuuuuuuuuuuuuuuiiiiiiii")
    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total' : grand_total
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
    current_user=request.user
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

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item =Cartitem.objects.get(product =product , cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('outgoing:cart')

def remove_item(request ,product_id):
    cart = Cart.objects.get(cart_id =_cart_id(request)) 
    product = get_object_or_404(Product, id=product_id)
    cart_item =Cartitem.objects.get(product=product, cart=cart)
    cart_item.delete()
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


def checkout(request ,total=0 ,cart_items=None):
    cart_items = [] 
    user= request.user
    user_pro , create=User_Profile.objects.get_or_create(user=user)
    user_profile_image_url=user_pro.image.url if user_pro.image else None
    user_pro.save()
    print("checkout_user:" , user)
    user_address=Address.objects.filter(user=request.user)
    print("checkout_:user_address" ,user_address)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for i in cart_items:
            total += (i.product.price * i.quantity)
        tax= ( 2 * total)/100
        grand_total = tax + total        
    except ObjectDoesNotExist:
        pass
    context={  
        'user_pro': user_pro,
        'user_address' :  user_address,
        'cart_items' : cart_items,
        'user_profile_image_url' : user_profile_image_url,
        'total': total,
        'grand_total': grand_total,
        'tax': tax
    }
    print(f'item:{cart_items}')
    print(f'userrrrr:{user}')
    print(f'user_address:{user_address}')
    print(f'user_pro:{user_pro}')
   
    return render (request , "checkout.html", context)


def new_address(request):
    if request.method=='POST':
        print(" if request.method=='POST':")
        count=Address.objects.filter(user=request.user).count()
        if count>=2:
            print("nooooooooooooooooooooooooooooiiiiiiiiii")
            messages.error(request, "Maximum of two addresses are allowed.")
            return redirect("outgoing:checkout")
        print("yasssssssssssssssss!!!!!!!!!!!!!!!")
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        country=request.POST.get('country')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip=request.POST.get('zip')
        print("get alllllllllllll")
        user_address=Address.objects.create(
            user=request.user,
            new_name=name,
            email=email,
            phone=phone,
            address=address,
            country=country,
            city=city,
            state=state,
            zip=zip
        )
        print("user_addresssssssssssssssssssssss saveeeeeeeeee")
        user_address.save()
        user_profile = User_Profile.objects.get(user=request.user)
        print("new user_profile:" , user_profile)
        data=Order()
        print("datttttttttaaaaaaa:", data)
        data.user=user_profile
        data.user_name=name
        data.address=address
        data.email=email
        data.phone=phone
        data.city=city
        data.state=state
        data.country=country
        data.ip=request.META.get('REMOTE_ADDR')
        data.save()
        print("data.usermmmmmmmmmmmmmm:" ,data.user)
        order_id =data.id
        print("order_id:",order_id)
        yr = int(datetime.date.today().strftime('%Y'))  # Use %Y instead of %y
        mt = int(datetime.date.today().strftime('%m'))
        dt = int(datetime.date.today().strftime('%d'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()
        print("datassssssss:", data.order_number)
        order=Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
        

        messages.success(request, "Successfully added")
        context={
            'order_id':order_id,
            'order':order,
        }
        return render(request, "checkout.html", context)
    print(" if request.method=='POST':noooooooooooooo")
    return redirect ("outgoing:checkout")

def delete_address(request,id):
    user_address=get_object_or_404(Address,id=id)
    user_address.delete()
    return redirect('outgoing:checkout')


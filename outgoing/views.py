import datetime
from datetime import date 
from django.urls import reverse
from django.utils import timezone
import uuid
import os
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from outgoing.models import Cart , Cartitem,Wishlist
from products.models import Product 
from orders.models import Order,Payment,OrderProduct
from accounts.models import User_Profile ,Address , Wallet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import paypalrestsdk
# paypalrestsdk.configure({
#     "mode": "sandbox",
#     "client_id":os.environ.get('PAYPAL_CLIENT_ID'),
#     "client_secret":os.environ.get('PAYPAL_CLIENT_SECRET')
# })import os
# import paypalrestsdk

# paypalrestsdk.configure({
#     "mode": "sandbox",  # or "live"
#     "client_id": os.environ.get('PAYPAL_CLIENT_ID'),
#     "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET')
# })

# # Check if client_id and client_secret are set
# if not os.environ.get('PAYPAL_CLIENT_ID') or not os.environ.get('PAYPAL_CLIENT_SECRET'):
#     raise Exception("PayPal client credentials are not set!")

paypalrestsdk.configure({
    "mode": "sandbox",  # or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

# Create your views here.
def cart(request, total=0, quantity=0, cart_item=None):
    if request.user.is_authenticated:
        print("in cart")

        cart_items = []  # Initialize cart_items as an empty list
        shipping = 0  # Initialize tax
        grand_total = 0  # Initialize grand_total
        wishlist_items=Wishlist.objects.filter(user=request.user)

        try:
            print("11111111111")
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                print("222222")
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            # tax= ( 2 * total)/100
            shipping = 40
            grand_total = shipping + total    
            print("suuuuuuuuuuuuuuuuuuuuuuuuuuuuuiiiiiiii")
        except ObjectDoesNotExist:
            pass
        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'wishlist_items':wishlist_items,
            'shipping': shipping,
            'grand_total' : grand_total
        }
        print(f'item:{cart_items}')
        print(f'total:{quantity}')
        print(f'total:{total}')

        return render(request,"cart.html", context)
    else:
        return redirect('accounts:userlogin')

def _cart_id(request):
    print("in cart_id+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    cart = request.session.session_key
    print("33333333333")
    if not cart:
        print("44444444444")
        cart= request.session.create()
    return cart

def add_cart(request,product_id):
    if request.user.is_authenticated:
        print("in add_cart+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        current_user=request.user
        product = Product.objects.get(id=product_id)#get product
        print("")
        try:
            print("555")
            cart=Cart.objects.get(cart_id=_cart_id(request))# get the cart using cart_id present in the session
        except Cart.DoesNotExist:
            print("666666")
            cart = Cart.objects.create(
                cart_id= _cart_id(request)
            ) 
        cart.save()
        print("add_cart....cart_save")
        try:
            print("88888888")
            cart_item =Cartitem.objects.get(product = product, user=current_user, cart = cart)
            cart_item.quantity += 1
            cart_item.save()
        except Cartitem.DoesNotExist:
            print("999999999")
            cart_item = Cartitem.objects.create(
                user = current_user,
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart = cart.save()
        Wishlist.objects.filter(user=request.user, product=product).delete()
        #return HttpResponse(cart_item.quantity)   
        return redirect('outgoing:cart')
    else:
        return redirect('accounts:userlogin')

def remove_cart(request, product_id):
    print("in remove_cart+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

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
    print("remove_item+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
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
    print("in checkout++++++++++++++++++++++++++++++++++++++++++++++++++++")
    cart_items = [] 
    user= request.user
    wishlist_items=Wishlist.objects.filter(user=request.user)
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
        shipping = 40
        grand_total = shipping + total 
         # Generate order ID
        order_number = generate_order_id()
        
        # Save order ID to session
        request.session['order_id'] = order_number
        print("checkout.order_number:",order_number)
    except ObjectDoesNotExist:
        pass
    payment_id = str(uuid.uuid4())
    request.session['payment_id'] = payment_id
    context={  
        'user_pro': user_pro,
        'user_address' :  user_address,
        'cart_items' : cart_items,
        'wishlist_items':wishlist_items,
        'user_profile_image_url' : user_profile_image_url,
        'total': total,
        'grand_total': grand_total,
        'tax': tax,
        'order_number': order_number,
        'payment_id': payment_id
    }
    print(f'item:{cart_items}')
    print(f'userrrrr:{user}')
    print(f'user_address:{user_address}')
    print(f'user_pro:{user_pro}')
    print(f'payment_id:{payment_id}')
    return render (request , "checkout.html", context)


def new_address(request):
    print("in new_address++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if request.method=='POST':
        print(" if request.method=='POST':")
        count=Address.objects.filter(user=request.user).count()
        if count>=2:
            messages.error(request, "Maximum of two addresses are allowed.")
            return redirect("outgoing:checkout")
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        country=request.POST.get('country')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip=request.POST.get('zip')
        print("ziiiiiiiiiiipp:", zip)
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
        user_address.save()
        messages.success(request, "Successfully added")
        return redirect("outgoing:checkout")
    print(" if request.method=='POST':noooooooooooooo")
    return redirect ("outgoing:checkout")

def delete_address(request,id):
    print("in delet_address++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    user_address=get_object_or_404(Address,id=id)
    user_address.delete()
    return redirect('outgoing:checkout')

def generate_order_id():
    print("in generate_order_id++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    unique_str = str(uuid.uuid4()).replace('-', '').upper()[:10]  # Generate a 10-character unique ID
    return unique_str

def place_order(request, total=0):
    print("in place_order+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if request.method == "POST":
        user = request.user
        print('user(place):',user)
        cart_items = Cartitem.objects.filter(user=user)
        user_wallet = User_Profile.objects.get(user=user)
        #order = Order.objects.filter(user=user , is_ordered=True, order_number=number).last()
        
        if cart_items.exists():
            # Get the address ID from the POST request
            address_id = request.POST.get('address')
            print('Address ID:', address_id)

            # Fetch the corresponding Address object
            address = get_object_or_404(Address, id=address_id)
            print('Address Details:', address)
            
            wishlist_items=Wishlist.objects.filter(user=request.user)

            payment_mode= request.POST.get("method")
            print("payment:", payment_mode)
            
            # Fetch the User_Profile instance associated with the current user
            user_profile = get_object_or_404(User_Profile, user=user)
            print('User Profile:', user_profile)

            order_number = request.session.get('order_id')
            print('Order Number:', order_number)

            if not order_number:
                # Handle the case where order_number is not found in session
                print('Order number not found in session')
                return redirect('outgoing:checkout')
            
            for i in cart_items:  # Line 29
                total += (i.product.price * i.quantity)  # Line 30
            shipping = 40
            grand_total = total + shipping  # Line 41
            print("grand_total:",grand_total)
            # Proceed with your order placement logic
            print("orders create (place)")
            orders = Order.objects.create(
                user=user_profile,
                address=address.address,
                user_name=address.new_name,
                email=address.email,
                phone=address.phone,
                city=address.city,
                state=address.state,
                country=address.country,
                zip=address.zip,
                order_number=order_number,
                order_total=grand_total
            )
            print("order_number(place):", orders.order_number)
            orders.save()
            payment_id = request.session.get('payment_id')
            print('payment_id:', payment_id)


            # order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
            if payment_mode=="cod":
                print("coooooooooooooooooooooooood")
                # order=(
                #     orders.last()

                # )
                payment=Payment(
                user=user_profile,
                method=payment_mode,
                status="pending",
                amount=orders.order_total
            )
                payment.save()
            else:
                payment=Payment(
                user=user_profile,
                method=payment_mode,
                payment_id=payment_id,
                status="completed",
                amount=orders.order_total
                )
                if payment_mode == "paypal":
                    print("if paypalllllllllllllllllllllllllllllllllllllllllllllllll")
                    request.session['payment_id']=payment_id




                    return redirect('outgoing:paypal_payment')
                    
                else:
                    
                    wallet_history=Wallet(
                    user=request.user,
                    )

                    wallet_history.save()

                    wallet_qs = Wallet.objects.filter(user=request.user)
                    print("wallet_qs:",wallet_qs)
                    if not wallet_qs.exists():
                        data= "no wallet found for the user"
                        return JsonResponse({"status": data})
                    wallet_instance=wallet_qs.first()
                    wallet_balance=wallet_instance.wallet_balance
                    if orders.order_total > wallet_balance:
                       data = ' You Do Not Sufficient Balance'
                       return JsonResponse({"status": data})
                    wallet_balance -= orders.order_total
                    wallet_instance.save()
                    wallet_history.transaction="DEBIT"
                    wallet_history.wallet_balance=wallet_balance
                    wallet_history.amount=orders.order_total
                    wallet_history.save()
                    print("wallet_history:",wallet_history)
                payment.save()
                orders.is_ordered= True
                print("payment_id:",payment_id)

            orders.payment=payment
            orders.save()
            for item in cart_items:
                order_product=OrderProduct(
                    user=user_profile,
                    order=orders,
                    payment=payment,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                order_product.save()
            Cartitem.objects.filter(user=request.user).delete()
            print("Cartitem_delet:" , Cartitem)
                # product = Product.objects.get(id=item.id)
                # product.stock -= item.quantity
                # product.save()

           


            
            subject="Thank You For Your Order"
            message= render_to_string(
                "recieved_mail.html", { "user":user_profile , "order":orders}

            ) 
            to_mail=request.user.email
            send_mail=EmailMessage(subject , message, to=[to_mail])
            send_mail.send()

            order_products = OrderProduct.objects.filter(order=orders, user=user_profile)
            
            context = {
                    "order_products": order_products,
                    "payment_id":payment_id,
                    "orders":orders,
                    "total" : total,
                    'wishlist_items':wishlist_items,
                }


            # order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
            # print(".............",order.user_name, order.order_number,order.status, order.phone, order.address, order.city, order.state, order.country)

            # Clear the cart items after placing the order (example logic)
            
            
            # cart_items.delete()

            # Redirect to checkout or order summary page
        
            return render(request, "order_success.html" , context)
        else:
            return redirect('shop:shop')
    else:
        # Handle cases where the request method is not POST
        print('Invalid request method')
        return HttpResponseRedirect('/')
def paypal_payment(request):
    print("paypal_paymnet")
    order_id = request.session.get('order_id')
    print('Order Number:', order_id)

    if not order_id:
                # Handle the case where order_number is not found in session
        print('Order number not found in session')
        return redirect('outgoing:checkout')
            
    cart_items = Cartitem.objects.filter(user=request.user)
    total=0
    for i in cart_items:
        total += (i.product.price * i.quantity)  # Line 30
        shipping = 40
        grand_total = total + shipping  # Line 41
        print("grand_total:",grand_total)
    total_bill=grand_total
    paypal_order={
        "intent":"sale",
        "payer":{
            "payment_mode": "paypal",

        },
        "redirect_urls":{
            "return_url":request.build_absolute_uri(reverse("outgoing:paypal_success")),
            "cancel_url":request.build_absolute_uri(reverse("outgoing:paypal_cancel"))
        },
        "transactions":[{
            "amount":{
                "total":str(total_bill),
                "currency":"USD"
            },
            "description":"Payment for order #"+str(order_id)
        }]
    }
    request.session['paypal_order']=paypal_order
    return redirect('outgoing:paypal_redirect')


# def paypal_redirect(request):
#     print("paypal_rediarect")
#     client_id=settings.PAYPAL_CLIENT_ID
#     client_secret=settings.PAYPAL_CLIENT_SECRET
#     paypal_sdk_client=paypalrestsdk.Api({
#         "mode":"sandbox",
#         "client_id":client_id,
#         "client_secret":client_secret

#     })
#     paypal_order=request.session['paypal_order']
     
#     paypal_order["redirect_urls"] = {
#         "return_url": request.build_absolute_uri(reverse("outgoing:paypal_success")),
#         "cancel_url": request.build_absolute_uri(reverse("outgoing:paypal_cancel")),  # Ensure this is correct
#     }

#     payment=paypalrestsdk.Payment(paypal_order)
#     if payment.create():
#         for link in payment.links:
#             if link.rel== 'approval_url':
#                 redirect_url=str(link.href)
#                 return redirect(redirect_url)

#     else:
#         messages.error(request,'paymant processing failed,please try again later')
#         return redirect('outgoing:checkout')
# def paypal_redirect(request):
#     print("paypal_redirect")
    
#     # Get PayPal client credentials
#     client_id = settings.PAYPAL_CLIENT_ID
#     client_secret = settings.PAYPAL_CLIENT_SECRET
    
#     # Configure PayPal SDK
#     paypalrestsdk.configure({
#         "mode": "sandbox",  # or "live"
#         "client_id": client_id,
#         "client_secret": client_secret
#     })
    
#     # Ensure paypal_order exists in session
#     if 'paypal_order' not in request.session:
#         messages.error(request, 'No PayPal order found in session.')
#         return redirect('outgoing:checkout')
    
#     paypal_order = request.session['paypal_order']
    
#     # Set return and cancel URLs
#     paypal_order["redirect_urls"] = {
#         "return_url": request.build_absolute_uri(reverse("outgoing:paypal_success")),
#         "cancel_url": request.build_absolute_uri(reverse("outgoing:paypal_cancel")),
#     }

#     # Create payment
#     payment = paypalrestsdk.Payment(paypal_order)
#     print("rediarectttttttttt",payment)
#     if payment.create():
#         for link in payment.links:
#             if link.rel == 'approval_url':
#                 redirect_url = str(link.href)
#                 return redirect(redirect_url)
#     # else:
#     #     messages.error(request, 'Payment processing failed, please try again later.')
#     #     return redirect('outgoing:checkout')
#     else:
#         print("Client ID:", client_id)
#         print("Client Secret:", client_secret)
#         print("PayPal order data:", paypal_order)
#         print("Payment object:", payment)


#         print("Payment failed:", payment.error)  # Add this line to print the error message
#         messages.error(request, 'Payment processing failed, please try again later.')
#         return redirect('outgoing:checkout')


def paypal_redirect(request):
    print("paypal_redirect")
    
    # Get PayPal client credentials
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    
    # Configure PayPal SDK
    paypalrestsdk.configure({
        "mode": "sandbox",  # or "live"
        "client_id": client_id,
        "client_secret": client_secret
    })
    
    # Ensure paypal_order exists in session
    if 'paypal_order' not in request.session:
        messages.error(request, 'No PayPal order found in session.')
        return redirect('outgoing:checkout')
    
    paypal_order = request.session['paypal_order']
    
    # Set return and cancel URLs
    paypal_order["redirect_urls"] = {
        "return_url": request.build_absolute_uri(reverse("outgoing:paypal_success")),
        "cancel_url": request.build_absolute_uri(reverse("outgoing:paypal_cancel")),
    }
    
    # Fixing payment_method field
    paypal_order['payer'] = {
        "payment_method": "paypal"
    }

    # Create payment
    payment = paypalrestsdk.Payment(paypal_order)
    print("Payment object:", payment)
    
    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        print("Payment failed:", payment.error)  # Print the error details
        messages.error(request, 'Payment processing failed, please try again later.')
        return redirect('outgoing:checkout')


# def paypal_success(request):
#     print("paypal_sucsses")
#     payer_id=request.Get.get('payerID')
#     order_id=request.session.get('order_id')
#     paypal_std_clint=paypalrestsdk.Api(
#         {
#             "mode":"sandbox",
#             "client_id":settings.PAYPAL_CLIENT_ID,
#             "client_secret":settings.PAYPAL_CLIENT_SECRET
#         }

#     )
#     payment=paypalrestsdk.Payment.find(request.GET["paymentId"])
#     if payment.execute({"payer_id":payer_id}):
#         order=Order.objects.get(id=order_id)
#         order.ORDER_STATUS=5
#         order.save()
#         del request.session['order_id']
#         del request.session['paypal_order']
#         messages.success(request,"payment processed successfully")
#         return render(request,'order_success.html',{'order':order})
#     else:
#         messages.error(request,'paymant processing failed,please try again later')
#         return redirect('outgoing:checkout')

# def paypal_cancel(request):
#     print("paypal_cancel")
#     messages.error(request,'payment was cancelled')
#     return redirect('outgoing:checkout')


# def paypal_success(request):
#     print("paypal_success")
#     payer_id = request.GET.get('PayerID')  # Make sure this matches the query parameter exactly
#     order_id = request.session.get('order_id')
#     paypal_std_client = paypalrestsdk.Api(
#         {
#             "mode": "sandbox",
#             "client_id": settings.PAYPAL_CLIENT_ID,
#             "client_secret": settings.PAYPAL_CLIENT_SECRET
#         }
#     )
    
#     payment = paypalrestsdk.Payment.find(request.GET.get("paymentId"))  # Correct key name here as well
#     if payment.execute({"payer_id": payer_id}):
#         order = Order.objects.get(id=order_id)
#         order.ORDER_STATUS = 5
#         order.save()
#         del request.session['order_id']
#         del request.session['paypal_order']
#         messages.success(request, "Payment processed successfully")
#         return render(request, 'order_success.html', {'order': order})
#     else:
#         messages.error(request, 'Payment processing failed, please try again later')
#         return redirect('outgoing:checkout')
def paypal_success(request):
    payer_id = request.GET.get('PayerID')
    order_id = request.session.get('order_id')

    print(f"order_id: {order_id}, type: {type(order_id)}")
 
    if not order_id:
        messages.error(request, 'Order ID not found in session.')
        return redirect('outgoing:checkout')

    paypal_std_client = paypalrestsdk.Api(
        {
            "mode": "sandbox",
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        }
    )

    payment = paypalrestsdk.Payment.find(request.GET.get("paymentId"))
    if payment.execute({"payer_id": payer_id}):
        try:
            order = Order.objects.get(order_number=order_id)  # Assuming order_number is the field to query
            order.ORDER_STATUS = 5
            order.save()
            Cartitem.objects.filter(user=request.user).delete()
            del request.session['order_id']
            del request.session['paypal_order']
            messages.success(request, "Payment processed successfully")
            return render(request, 'order_success.html', {'order': order})
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('outgoing:checkout')
    else:
        messages.error(request, 'Payment processing failed, please try again later')
        return redirect('outgoing:checkout')

def paypal_cancel(request):
    print("paypal_cancel")
    messages.error(request, 'Payment was cancelled')
    return redirect('outgoing:checkout')





def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items=Wishlist.objects.filter(user=request.user)
        return render (request,"wishlist.html",{'wishlist_items':wishlist_items})
    else:
        return redirect("accounts:userlogin")
def add_to_wishlist(request,product_id):
    if request.user.is_authenticated:
        product=get_object_or_404(Product, id=product_id)
        Wishlist.objects.get_or_create(user=request.user,product=product)
        return redirect("outgoing:wishlist_view")
    else:
        return redirect("accounts:userlogin")

def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Wishlist, user=request.user, product__id=product_id)
    product.delete()
    
    return redirect("outgoing:wishlist_view")

# def cash_on_delivery(request,number):
#     print("COD+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#     orders=Order.objects.filter(user=request.user, is_ordered=False, order_number=number)

    
#     user_profile=get_object_or_404(User_Profile , user=request.user)
#     if orders.exists():
#         print("hhhhhhhhhhhhhhhhhhhhhhhhaaaaaaaaaaaaaaaaiiiiiiiiii")
#         order=(
#             orders.last()
#         )
#         payment =Payment(
#             user=user_profile,
#             payment_id=number,
#             method="COD",
#             status="Completed",

#         )
#         payment.save()
#         order.payment=payment
#         order.is_ordered = True
#         order.save()
#         cart_item = Cartitem.objects.filter(user=request.user)
#         for item in cart_item:
#             order_product = OrderProduct()
#             order_product.order=order
#             order_product.payment=payment
#             order_product.user=user_profile
#             order_product.product=item.product
#             order_product.price=item.product.price
#             order_product.quantity=item.quantity
#             order_product.save()

#            # Reduce the quantity of sold product
#             # product = Product.objects.get(id=item.product_id)
#             # product.stock -= item.quantity
#             # product.save()
#         Cartitem.objects.filter(user=request.user).delete()
#             # order_products = OrderProduct.objects.filter(order=order, user=user_profile)
        
#             # context = {
#             #     "order_products": order_products,
#             #     }
#         return redirect("outgoing:checkout")
#     return redirect("outgoing:checkout") 
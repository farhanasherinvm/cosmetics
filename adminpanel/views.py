from django.contrib.auth import authenticate,login
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.cache import never_cache
from accounts.models import User_Profile
from products.models import Product
from category.models import Category
from django.utils.text import slugify
# Create your views here
@never_cache
def admlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_obj = authenticate(username=username,password=password)
        if user_obj is not None:
            if user_obj.is_superuser:
                login(request,user_obj)
                return redirect ('adminpanel:dashboard')
            else:
                context={
                    'error': "user is not authenticated"}
                return render(request,'admlogin.html',context)
            
        else:
            messages.error(request,"invalid credentials")

    return render(request,"admlogin.html")

@never_cache
def admlogout(request):
    return render(request,"admlogin.html")


def dashboard(request):
    return render(request,"dashboard.html")


def user_manage(request):
    user=User_Profile.objects.all()
    print(f"she:",user)
    context={
        'user':user,
    }
    print("sec:",user)
    return render(request,"all_users.html",context)

def user_block(request,id):
    user=get_object_or_404(User_Profile,id=id)

    if user.is_active:
        
        user.is_active=False
        user.save()
        
    else:
        print("!!!!!!!!!!!!!!!!!!!!")
        user.is_active=True
        user.save()
    return redirect('adminpanel:user_manage')



# def newuser(request):
#     return render(request,"add_newuser.html")

def product_manage(request):
    product= Product.objects.all()
    category=Category.objects.all()

    context={
        'product':product,
        'category':category
    }
    return render(request,'product.html',context)

def add_product(request):
    if request.method=='POST':
        product_name=request.POST.get('name')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        price=request.POST.get('price')
        stock=request.POST.get('stock')
        category_name=request.POST.get('category')

        category_instance, created= Category.objects.get_or_create(category_name=category_name)
        slug = slugify(product_name)
        new_product=Product.objects.create(
            product_name=product_name,
            description=description,
            image=image,
            price=price,
            stock=stock,
            category=category_instance,
            slug=slug
        )
        new_product.save()
        return redirect('adminpanel:product_manage')
    return render(request,'product.html')   

# def delete_product(id):
#     product = Product.objects.get(id=id)
#     product.delete()
#     return redirect('product_manage')
    
# def product_list(request,id):
#     item=get_object_or_404(Product,pk=id)
#     item.is_available=True
#     item.save()
#     return redirect('product_manage')
# def product_unlist(request,id):
#     item=get_object_or_404(Product,pk=id)
#     item.is_available=False
#     item.save()
#     return redirect('product_manage')


def product_list(request, id):
    product = get_object_or_404(Product, id=id)
    if product.is_available:
       
        product.is_available = False
        product.save()
    else:
       
        product.is_available = True
        product.save()
    return redirect('adminpanel:product_manage')

def edit_product(request):
    if request.method=='POST':
        product_id = request.POST.get('product_id')
        product_name=request.POST.get('edit_name')
        description=request.POST.get('edit_description')
        image=request.FILES.get('edit_image')
        stock=request.POST.get('edit_stock')
        category=request.POST.get('category')
        price=request.POST.get('edit_price')
          
        category_instance = Category.objects.get(id=category)

        update=get_object_or_404(Product, id=product_id)
        update.product_name=product_name
        update.description=description
        if image:
            update.image=image
        update.stock=stock
        update.price=price
        update.category= category_instance
        update.save()
        return redirect('adminpanel:product_manage')
    return redirect('adminpanel:product_manage')


def category_manage(request):
    category = Category.objects.all()
    
    context = {
        'category': category ,
    }
    return render(request,"category.html",context)


def add_category(request):
    if request.method == 'POST':
        
        category_name = request.POST.get('name')
        category_description = request.POST.get('description')
        category_image = request.FILES.get('image')
        
        new_category = Category(
            slug = slugify(category_name),
            category_name=category_name,
            category_description=category_description
        )

        if category_image:
            new_category.category_image = category_image

        new_category.save()
        return redirect('adminpanel:category_manage')

    return render(request, 'category.html')

def category_delete(request, category_id):
    category=get_object_or_404(Category,id=category_id)
    category.delete()
    return redirect('adminpanel:category_manage')

# def edit_category(request):
#     if request.method=='POST':
#         print("!!!!!!!!!!!!!!!!!!!")
#         category_id=request.POST.get('category_id')
#         print("!!!!!!!!!a!!!!!!!!!!")
#         if not category_id:
#             return HttpResponseBadRequest("Category ID is missing in the form data.")

#         name=request.POST.get('edit_name')
#         print("!!!!!!!!!!b!!!!!!!!!")
#         description=request.POST.get('edit_description')
#         image=request.FILES.get('edit_image')

#         update=get_object_or_404(Category, id=category_id)
#         update.category_name=name
#         update.category_description=description
#         update.category_image=image
#         update.save()

#     return redirect('adminpanel:category_manage')






def edit_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
            
        category_name = request.POST.get('edit_name')
        category_image = request.FILES.get('edit_image')
        description = request.POST.get('edit_description')
        update = get_object_or_404(Category, id=category_id)
        update.category_name = category_name
        if category_image:
            update.category_image = category_image
        update.category_description = description
        
        update.save()
        messages.success(request, 'Category updated successfully')
        return redirect('adminpanel:category_manage')
    else:
        return redirect('adminpanel:category_manage') 
   

def order_detail(request):
    return render (request,"order_detail.html")
def orders(request):
    return render (request,"orders.html")

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from products.models import Category, Product
# Create your views here.

from django.shortcuts import render, redirect


def usersignup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        if username and password and email:
            usr_obj = User.objects.create_user(username=username,password=password,email=email)
            usr_obj.save()
            return redirect('userlogin')
        else:
            
            return render(request, "signup.html", {'error_message': 'Please fill in all required fields'})

    return render(request, "signup.html")

def user_otp(request):
    return render(request,'otp.html')

@never_cache
def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('usersignup')
    return render(request,"login.html")

def userlogout(request):
    return render(request,"login.html")

def home(request):
    
    product=Product.objects.all()
    category=Category.objects.all()

    context={
        'product':product,
        'category':category,
    }
    return render(request,"home.html",context)

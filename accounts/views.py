import random
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from accounts.forms import SignUpForm
from django.contrib import messages
from accounts.models import User_Profile,Address
# Create your views here.
def user_otp(request):
    if request.method=='POST':
        print("EEEEEEEEEEEEEEEEEEEEEEEE")
        print(request.POST)
         # Print individual otp_entered values
        for i in range(1, 7):
            print(f"otp_entered_{i}: {request.POST.get(f'otp_entered_{i}', '')}")
        
        # Concatenate individual otp_entered values into a single string
        otp_entered = "".join(request.POST.get(f'otp_entered_{i}', '') for i in range(1, 7))
        
        otp_saved = str(request.session.get('signup_otp'))   
        print(otp_entered,otp_saved)
        if otp_entered == otp_saved:
            print("88888888888888888888888888888888888")
            del request.session['signup_otp']
            username=request.session['signup_username']
            print("1111111111111111111111")
            user=User.objects.get(username=username)
            user.is_active=True
            user.is_otp=True
            user.save()
            messages.success(request, "Your registration is successful. You can now log in.")
            return redirect('accounts:userlogin')
    return render(request,'otp.html')


def new_otp(request):
    username=request.session.get("signup_username")
    user=User.objects.get(username=username)
    request.session.pop("signup_otp",None)
    if user.email:
        otp=str(random.randint(100000,999999))
        request.session["signup_otp"]=otp
        subject= 'otp verfication code'
        massage=f'your otp code for signup is: {otp}'
        from_email='farhanashnz@gmail.com'
        recipient_list=[user.email]
        send_mail (subject,massage,from_email,recipient_list)
        messages.success(request, 'resend OTP sent successfully. Please check your email.')
    else:
        messages.warning(request, 'Failed to resend OTP. Please try again.')
    return render(request,'otp.html')


def usersignup(request):
    if request.method == 'POST':
        # username = request.POST.get('username', '')
        # password = request.POST.get('password', '')
        # email = request.POST.get('email', '')

        # if username and password and email:
        #     print("!!!!!!!!!!")
        #     usr_obj = User.objects.create_user(username=username,password=password,email=email)
        #     usr_obj.save()
        print("!!!!!!!!!!!!!!!!!!!!!!!")
        form = SignUpForm(request.POST)
        print("aaaaaaaaaaaaaaa:", form)

        if form.is_valid():
            print("bbbbbbbbbbbb")
            form.save()
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            email=form.cleaned_data.get('email')
            otp= str(random.randint(100000 ,999999))
            request.session['signup_username']=username
            request.session['signup_otp']=otp
            subject= 'otp verfication code'
            massage=f'your otp code for signup is: {otp}'
            from_email='farhanashnz@gmail.com'
            recipient_list=[email]
            send_mail (subject,massage,from_email,recipient_list)
            print("yyyyyyyyyyyyyyy")
            messages.success(request,'Your account has been created!Please Enter OTP')
            return redirect('accounts:otp')
        else:
            messages.warning(request,form.errors)
            print("cooooooooooooooooooooooool")
            return redirect('accounts:usersignup')
    return render(request, "signup.html")



@never_cache
def userlogin(request):
    if request.method=='POST':
        email = request.POST.get('email', '')  # Provide an empty string as the default value
        password = request.POST.get('password', '')
        print('email:', email)
        user= authenticate(request, email=email, password=password)
        print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        if user is not None:
            print("not none")

            if user.email != email:
                messages.error(request, 'Invalid Credentials')
                print("tttttttttt")

                return render(request, 'login.html')
            
            if user:
                user_pro, created = User_Profile.objects.get_or_create(user=user)
                user_pro.email = email
                user_pro.user_name
                print(user_pro.email,"___________________________")
                user_pro.save()

            login(request,user)
            return redirect('accounts:edit_profile')
        else:
            print("not ifffffffffffff")
            return render(request,"login.html")
    return render(request,"login.html")

def userlogout(request):
    logout(request)
    return redirect("home:home")

def profile(request):
    print("check")
    if request.user.is_authenticated:

        user=request.user
        print("user:",user)
        user_pro ,created= User_Profile.objects.get_or_create(user=user)
        user_pro_image_url = user_pro.image.url if user_pro.image else None
        print("pro:||||||||||||",user_pro)
        print('procreated:',created)
        context={
            'user_pro': user_pro,
         
            'user_pro_image_url' : user_pro_image_url
        }
        print('created:',created)
        print( 'user_pro:' ,user_pro.user_name)
        return render(request,"profile.html",context)
    return render(request,"login.html")


def edit_profile(request):
    if request.method=='POST': 
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        number = request.POST['number']
        image = request.FILES.get('image')
      
        print("username:" , username)
        print("email:",email)
        print("number:", number)

        user_form , created = User.objects.get_or_create(username=username)
        user_form.email = email
        user_form.first_name= first_name
        user_form.last_name = last_name
        user_form.save()
        print("user_form",user_form.email)
       
        profile , created= User_Profile.objects.get_or_create(user=user_form)
        print("after:",profile)
        profile.phone= number
        print("phoneeeeeee:",profile.phone)
        if image:
            profile.image = image
        return redirect('accounts:profile')
    else:
        user_form=request.user
        profile ,created = User_Profile.objects.get_or_create(user=user_form)

        context={
            'user_form':user_form,
            'profie': profile
        }
    return render(request, "edit_profile.html", context)

def address(request):
    user_pro ,created = User_Profile.objects.get_or_create(user=request.user)
    user_address= Address.objects.filter(user=request.user)
    context={
        'user_pro':user_pro,
        'user_address':user_address
    }
    return render(request ,"checkout.html" ,context)

def edit_address(request):
    return render(request,"checkout.html")
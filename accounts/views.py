import random
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from accounts.forms import SignUpForm
from django.contrib import messages

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
        print("aaaaaaaaaaaaaaa")
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
        user=authenticate(request, email=email, password=password)
        if user is not None:
            print("not none")

            if user.email != email:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'login.html')
            print("tttttttttt")
            login(request,user)
            return redirect('home:home')
        else:
            return render(request,"login.html")
    return render(request,"login.html")

def userlogout(request):
    logout(request)
    return redirect("home:home")

def edit_profile(request):
    if request.method=='POST': 
        first_name = request.POST.get('first name')
        last_name = request.POST.get('Last Name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        image = request.FILES.get('image')
        

    return render(request, "edit_profile.html")
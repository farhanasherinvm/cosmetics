from django.shortcuts import redirect, render

# Create your views here.

# def recieved_mail(request):
#     return render (request ,"recieved_mail.html")
def order_tracking(request):
    return render(request, "order_tracking.html")
def cash_on_delivery(request):
    return redirect ('outgoing:checkout')
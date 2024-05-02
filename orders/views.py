from django.shortcuts import render

# Create your views here.

def order_success(request):
    return render (request ,"order_success.html")
def order_tracking(request):
    return render(request, "order_tracking.html")
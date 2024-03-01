"""
URL configuration for cosmetics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/', include('adminpanel.urls', namespace='adminpanel')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('',include('home.urls')),
    path('',include('category.urls')),
    path('',include('products.urls')),
    path('outgoing/', include('outgoing.urls', namespace='outgoing')),
      path('cart/', include('outgoing.urls', namespace='cart')),  # Assuming you have a separate 'cart' app
    path('products/', include('products.urls', namespace="products"))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
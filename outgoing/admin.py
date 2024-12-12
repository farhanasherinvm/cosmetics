from django.contrib import admin

from.models import Cart
from.models import Cartitem,Wishlist

# Register your models here.
admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(Wishlist)
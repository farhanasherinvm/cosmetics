from django.contrib import admin

from.models import Cart
from.models import Cartitem

# Register your models here.
admin.site.register(Cart)
admin.site.register(Cartitem)
from django.contrib import admin
from .models import User_Profile, Address, Wallet

# Register your models here.

class User_ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone' ,'image')

admin.site.register(User_Profile,User_ProfileAdmin)
admin.site.register(Address)
admin.site.register(Wallet)
from django.contrib import admin
from.models import Product, ProductVariant,SideImage
# Register your models here.


class SideImageInline(admin.TabularInline):
    model = SideImage
    extra = 1  # Number of empty side image forms to display in the admin

class ProductAdmin(admin.ModelAdmin):
    inlines = [SideImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(SideImage)
admin.site.register(ProductVariant)

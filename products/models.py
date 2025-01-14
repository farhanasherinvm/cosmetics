from django.db import models
from django.urls import reverse
from category.models import Category


class Product(models.Model):
    product_name = models.CharField(max_length=50,unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    description  = models.TextField(max_length=500)
    price        = models.DecimalField(max_digits=10,decimal_places=2)
    image        = models.ImageField(upload_to='photos/products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('products:product', args=[self.slug, self.id])

    def __str__(self):
        return self.product_name


class SideImage(models.Model):
    product = models.ForeignKey(Product, related_name='side_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/side_images' ,blank=True, null=True)  # Additional image for the variant

    def __str__(self):
        return self.product.product_name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product,related_name='variants',on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='photos/variants' , blank=True, null=True)
    color   = models.CharField(max_length=100)
    price   = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    stock   = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.product_name} - {self.color}"
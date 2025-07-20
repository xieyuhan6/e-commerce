from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self)->str:
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category,related_name="products",on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="products",blank=True)
    
    def __str__(self)->str:
        return self.name
    def get_absolute_url(self):
        return reverse("products:product_detail",kwargs={"id":self.id,"slug":self.slug })
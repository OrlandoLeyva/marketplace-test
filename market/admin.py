from django.contrib import admin
from .models import Product, Category, Review, ProductCategory

# Register your models here.
admin.site.register((Product, Category, Review, ProductCategory))
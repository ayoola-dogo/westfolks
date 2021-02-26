from django.contrib import admin
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    fields = ('company', 'product_name', 'category', 'description', 'image', 'url')


admin.site.register(Product, ProductAdmin)

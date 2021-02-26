from django import forms
from .models import Product
from company.models import Company


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'image', 'url']

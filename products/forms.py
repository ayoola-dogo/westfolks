from django import forms
from .models import Product
from company.models import Company
import os
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'image', 'url']


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xlsx', '.xlsm', '.xltx', '.xltm', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UploadExcelForm(forms.Form):
    title = forms.CharField(max_length=70, required=True, initial="File Name")
    file = forms.FileField(required=True, validators=[validate_file_extension])

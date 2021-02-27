from django import forms
from .models import Company


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'logo', 'mantra', 'description', 'website_url']

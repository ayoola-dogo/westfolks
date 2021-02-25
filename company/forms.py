from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Company


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_logo', 'company_mantra', 'company_description']

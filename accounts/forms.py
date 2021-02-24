from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

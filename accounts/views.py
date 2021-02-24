from django.shortcuts import render
from django.views import View
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate


# Create your views here.
class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        user_form = self.form_class()
        context = {'user_form': user_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        context = {'user_form': user_form}
        if user_form.is_valid():
            new_user = user_form.save()
            new_user.refresh_from_db()
            new_user.save()
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('user:login'))
        return render(request, self.template_name, context)

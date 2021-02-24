from django.shortcuts import render
from django.views import View
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import pytz
from django.core import exceptions
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model


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


class UserProfileView(View):
    template_name = 'accounts/view_your_account.html'

    @method_decorator(login_required)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # User will be directed to the profile page after logging in
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            context = {}
            return render(request, self.template_name, context=context)
        else:
            return HttpResponseRedirect(reverse('accounts:register'))

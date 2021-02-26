from django.shortcuts import render
from django.views import View
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import pytz
from company.models import Company


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
            if request.user.account.company:
                company = Company.objects.get(account=request.user.account)
                context = {'company': company}
            else:
                context = {}
            return render(request, self.template_name, context=context)
        else:
            return HttpResponseRedirect(reverse('accounts:register'))

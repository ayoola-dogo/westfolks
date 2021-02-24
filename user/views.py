from django.shortcuts import render, reverse
from django.views import View
from .forms import UserLoginForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from .models import User


# Create your views here.
class LoginView(View):
    form_class = UserLoginForm
    template_name = 'user/access_your_account.html'
    redirect_field_name = 'accounts:profile'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return HttpResponseRedirect(reverse(self.redirect_field_name))
        user_form = self.form_class()
        context = {'user_form': user_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse(self.redirect_field_name))
            else:
                return HttpResponse("Account has been closed")
        user_form = self.form_class()
        context = {'user_form': user_form}
        return render(request, self.template_name, context)

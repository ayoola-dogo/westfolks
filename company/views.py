from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateCompanyForm
from products.forms import ProductForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from company.models import Company
from django.utils import timezone
from .com_files import move_company_image


# Create your views here.
class CreateCompanyView(View):
    form_class = CreateCompanyForm
    template_name = 'company/create_a_company.html'
    redirect_field_name = 'company:view-company'

    @method_decorator(login_required)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        company_form = self.form_class()
        context = {'company_form': company_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        company = Company(account=request.user.account)
        company_form = self.form_class(request.POST, request.FILES, instance=company)
        context = {'company_form': company_form}
        if company_form.is_valid():
            company_form.save()
            comp_logo = move_company_image(request)
            return HttpResponseRedirect(reverse(self.redirect_field_name))
        return render(request, self.template_name, context)


class CompanyView(View):
    template_name = 'company/view_company.html'
    redirect_field_name = 'company:view-company'
    model = Company

    @method_decorator(login_required)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        company = self.model.objects.get(account=self.request.user.account)
        context = {'company': company}
        return render(request, self.template_name, context)

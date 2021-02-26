from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from .forms import CreateCompanyForm
from products.forms import ProductForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# Create your views here.
class CreateCompanyView(CreateView):
    form_class = CreateCompanyForm
    template_name = 'company/create_a_company.html'
    redirect_field_name = 'company:view-company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = self.request.user
        return context

    @method_decorator(login_required)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        company_form = self.form_class()
        context = {'company_form': company_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        company_form = self.form_class(request.POST)
        if company_form.is_valid():
            company_form.save()
            return HttpResponseRedirect(reverse(self.redirect_field_name))
        context = {'company_form': company_form}
        return render(request, self.template_name, context)

    def form_valid(self, comp_form):
        comp_form.instance.account = self.request.user
        return super().form_valid(comp_form)


class CompanyView(View):
    comp_form = CreateCompanyForm
    product_form = ProductForm
    template_name = 'company/view_company.html'

    @method_decorator(login_required)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        company_form = self.comp_form()
        product_form = self.product_form()
        context = {'company_form': company_form, 'product_form': product_form}
        return render(request, self.template_name, context)

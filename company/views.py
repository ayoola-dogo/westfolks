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
from .com_files import move_company_image, get_company_logo, get_logo_url
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView


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
            move_company_image(request)
            logo = get_logo_url(company, request.user.email)
            company.logo = logo
            company.save(update_fields=['logo'])
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


class UpdateCompanyView(SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CreateCompanyForm
    template_name = 'company/update_company.html'
    success_message = 'Your company data have been successfully updated'

    @method_decorator(login_required)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_active:
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            # Add more context to the context
            company = self.model.objects.get(account=self.request.user.account)
            company_form = CreateCompanyForm(instance=company)
            additional_context = {'company_form': company_form}
            context.update(additional_context)
            return context

    def get_success_url(self):
        move_company_image(self.request)
        company = Company.objects.get(account=self.request.user.account)
        logo = get_logo_url(company, self.request.user.email)
        company.logo = logo
        company.save(update_fields=['logo'])
        view_name = 'company:view-company'
        return reverse(view_name)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateCompanyForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


# Create your views here.
class CreateCompanyView(View):
    form_class = CreateCompanyForm
    template_name = 'company/create_a_company.html'
    redirect_field_name = 'company:view-company'

    @login_required
    def get(self, request, *args, **kwargs):
        company_form = self.form_class()
        context = {'company_form': company_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        company_form = self.form_class(request.POST)
        context = {'company_form': company_form}
        if company_form.is_valid():
            company_form.save()
            return HttpResponseRedirect(HttpResponseRedirect(reverse(self.redirect_field_name)))
        return render(request, self.template_name, context)


class CompanyView(View):
    pass

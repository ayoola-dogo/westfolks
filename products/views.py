from django.shortcuts import render
from django.urls import reverse
from .models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from company.models import Company
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
def search(request):
    try:
        k = request.GET.get('k')
    except Exception:
        k = None
    if k:
        products = Product.objects.filter(title__icontains=k)
        context = {'query': k, 'products': products}
        template = 'products/results.html'
    else:
        context = {}
        template = 'products/home.html'
    return render(request, template, context)


@login_required
def product_upload(request):
    template = 'products/product_upload.html'
    prod_form = ProductForm()
    context = {'prod_form': prod_form}

    if request.method == "GET":
        return render(request, template, context)

    if request.method == "POST":
        company = Company.objects.get(account=request.user.account)
        new_product = Product(company=company)
        prod_form = ProductForm(request.POST, instance=new_product)
        if prod_form.is_valid():
            prod_form.save()
            prod_count = company.product_set.all().count()
            return HttpResponseRedirect(reverse('products:product-success', kwargs={'num': prod_count}))
        return render(request, template, context)


def product_success(request, num):
    template = 'products/product_successful.html'
    context = {'prod_count': num}
    return render(request, template, context)


class ProductDetailView(DetailView):
    pass


class ProductListView(ListView):
    pass

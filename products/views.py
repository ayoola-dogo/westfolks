from django.shortcuts import render
from django.urls import reverse
from .models import Product
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import Product
from .forms import ProductForm, UploadExcelForm
from company.models import Company
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from spreadsheet.spreadsheet_processor import spreadsheet_db, write_product_from_db_spreadsheet, delete_uploaded_file
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from company.com_files import move_product_image, get_product_url
from django.core.exceptions import FieldDoesNotExist


# Create your views here.
# Search feature not yet implemented
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
        prod_form = ProductForm(request.POST, request.FILES, instance=new_product)
        if prod_form.is_valid():
            prod_form.save()
            write_product_from_db_spreadsheet(request, new_product)
            move_product_image(request)
            image = get_product_url(new_product, request.user.email)
            new_product.image = image
            # Could also use a setter in the model
            new_product.save(update_fields=['image'])
            prod_count = company.product_set.all().count()
            return HttpResponseRedirect(reverse('products:product-success', kwargs={'num': prod_count}))
        return render(request, template, context)


@login_required
def product_success(request, num):
    if request.user.is_authenticated:
        template = 'products/product_successful.html'
        context = {'prod_count': num}
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('user:login'))


@login_required
def spreadsheet_upload(request):
    template = 'products/spreadsheet_upload.html'

    if request.method == 'GET':
        excel_form = UploadExcelForm()
        context = {'excel_form': excel_form}
        return render(request, template, context)

    if request.method == 'POST':
        excel_form = UploadExcelForm(request.POST, request.FILES)
        if excel_form.is_valid():
            cd = excel_form.cleaned_data
            ext = os.path.splitext(str(request.FILES['file']))[1]
            with open('static/media/{}/resources/{}{}'.format(request.user.email, cd['title'], ext),
                      'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            return HttpResponseRedirect(reverse('products:spreadsheet-process'))
        else:
            excel_form = UploadExcelForm()
            context = {'excel_form': excel_form}
            return render(request, template, context)
    else:
        raise Http404


@csrf_exempt
def excel_processor(request):
    if request.user.is_authenticated and request.user.is_active:
        try:
            add_count = spreadsheet_db(request)
            company = Company.objects.get(account=request.user.account)
            prod_count = company.product_set.all().count()
            return HttpResponseRedirect(reverse('products:product-success', kwargs={'num': prod_count}))
        except (FieldDoesNotExist, AttributeError, KeyError):
            return HttpResponseRedirect(reverse('products:upload-error'))

    else:
        raise Http404


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'

    def get_object(self, **kwargs):
        return Product.objects.get(slug=self.kwargs['slug'])


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    ordering = ['pk']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(pk=self.kwargs['company_id'])
            if self.request.user.account == company.account:
                products = company.product_set.all().order_by('-id')[:10]
                context = {'products': products}
                return render(request, self.template_name, context)
            else:
                raise Http404
        except ObjectDoesNotExist:
            raise Http404


@login_required
def upload_error(request):
    template = 'products/product_upload_error.html'
    context = {}
    delete_uploaded_file(request)
    return render(request, template, context)

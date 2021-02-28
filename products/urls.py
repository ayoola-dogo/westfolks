from django.urls import path
from .views import ProductDetailView, ProductListView, product_upload, product_success, spreadsheet_upload, excel_processor


app_name = 'products'

urlpatterns = [
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-list/<int:company_id>', ProductListView.as_view(), name='product-list'),
    path('product-upload/', product_upload, name='product-upload'),
    path('product-success-uploaded/<int:num>', product_success, name='product-success'),
    path('spreadsheet-upload/', spreadsheet_upload, name='spreadsheet-upload'),
    path('spreadsheet-process/', excel_processor, name='spreadsheet-process')
]

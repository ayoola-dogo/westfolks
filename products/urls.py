from django.urls import path
from .views import ProductDetailView, ProductListView, product_upload, product_success


app_name = 'products'

urlpatterns = [
    path('product-detail/<pk>', ProductDetailView.as_view(), name='product-detail'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-upload/', product_upload, name='product-upload'),
    path('product-success-uploaded/<int:num>', product_success, name='product-success')
]

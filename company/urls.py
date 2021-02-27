from django.urls import path
from .views import CreateCompanyView, CompanyView, UpdateCompanyView


app_name = 'company'

urlpatterns = [
    path('create-company/', CreateCompanyView.as_view(), name='create-company'),
    path('your-company/', CompanyView.as_view(), name='view-company'),
    path('update-company/<int:pk>/', UpdateCompanyView.as_view(), name='update-company')
]

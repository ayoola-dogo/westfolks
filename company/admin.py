from django.contrib import admin
from .models import Company


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    fields = ('company_name', 'company_mantra')


admin.site.register(Company, CompanyAdmin)

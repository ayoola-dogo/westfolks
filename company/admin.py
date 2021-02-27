from django.contrib import admin
from .models import Company


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    fields = ('account', 'company_name', 'logo', 'mantra', 'description', 'website_url')


admin.site.register(Company, CompanyAdmin)

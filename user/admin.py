from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class UserCustomAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_staff', 'is_admin', 'is_active')
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ()
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        ('Login data', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'full_name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
        ('Additional data', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

    ordering = ['-date_joined']
    filter_horizontal = ()

    class Meta:
        model = User


admin.site.register(User, UserCustomAdmin)

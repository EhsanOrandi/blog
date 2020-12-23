from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import User
from django.utils.translation import gettext_lazy as _

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'is_staff']
    password_change_form = AdminPasswordChangeForm
    ordering = ['email', ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (_('authentication data'), {
            "fields": (
                'email',
                'password',
            ),
        }),
        (_('Personal info'), {
            "fields": ('full_name', 'avatar')
        }),
        (_('Permissions'), {
            "fields": ('is_staff', 'is_active', 'is_superuser',)
        }),
        (_('Important dates'), {
            "fields": ('last_login',)
        }),
    )



admin.site.register(User, UserAdmin)
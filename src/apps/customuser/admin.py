from apps.common.actions import export_as_excel
from apps.customuser.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    actions = (export_as_excel, )
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'email',
        'id',
        'first_name',
        'last_name',
        'date_created',
        'last_login',
        'is_active',
        'is_admin',
        'is_superuser',
    )
    list_filter = (
        'is_admin',
        'is_active',
    )
    fieldsets = (
        (None, {'fields': (
            'email',
            'password'
        )}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'date_created',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_admin',
            'is_superuser',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
            )
        }),
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )
    filter_horizontal = ()
    ordering = ('-date_created',)

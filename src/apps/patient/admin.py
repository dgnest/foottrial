from apps.common.actions import export_as_excel
from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    actions = (export_as_excel, )

    fields = (
        'code',
        'first_name',
        'dni',
        'cellphone',
        'birthday',
        'hospital',
    )
    list_display = (
        'id',
        'code',
        'first_name',
        'dni',
        'is_active',
        'cellphone',
        'birthday',
        'date_joined',
        'date_deactivate',
        'deactivate_reason',
        'hospital',
        'sms_scheduled',
        'total_sms',
        'sms_received',
        'sms_failed',
        'calls_scheduled',
        'total_calls',
        'calls_answered',
        'calls_failed',
    )
    list_filter = (
        'is_active',
        'hospital',
        'deactivate_reason',
    )
    search_fields = (
        'first_name',
        'cellphone',
        'code',
        'dni',
    )
    ordering = ('-date_joined',)

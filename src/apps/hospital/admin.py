from apps.common.actions import export_as_excel
from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    actions = (export_as_excel, )

    fields = (
        'name',
        'abbrev',
        'doctor',
        'phone',
    )
    list_display = (
        'name',
        'abbrev',
        'doctor',
        'phone',
        'date_created',
    )
    search_fields = (
        'name',
        'abbrev',
        'doctor',
        'phone',
    )
    ordering = ('-date_created',)

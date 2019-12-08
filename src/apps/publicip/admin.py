from django.contrib import admin
from .models import PublicIP


@admin.register(PublicIP)
class PublicIPAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'public_ip',
    )
    ordering = ('-date_updated',)

from apps.common.actions import export_as_excel
from django.contrib import admin
from .models import Message, MessagingSchedule


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    actions = (export_as_excel, )

    fields = (
        'order',
        'type_message',
        'message',
        'track_file',
    )
    list_display = (
        'id',
        'order',
        'type_message',
        'message',
        'date_created',
        'total_sms',
        'sms_received',
        'sms_failed',
        'total_calls',
        'calls_answered',
        'average_call_time',
        'player',
    )
    list_filter = (
        'order',
        'type_message',
    )
    search_fields = (
        'message',
    )
    ordering = ('id',)

    def player(self, instance):
        return """
        <audio controls>
            <source src="%s" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        """ % instance.track_file.url

    player.allow_tags = True
    player.admin_order_field = 'track_file'


@admin.register(MessagingSchedule)
class MessagingScheduleAdmin(admin.ModelAdmin):
    actions = (export_as_excel, )

    fields = (
        'message',
        'patient',
        'parsed_message',
        'type_message',
        'date_scheduled',
    )
    list_display = (
        'message',
        'patient',
        'parsed_message',
        'type_message',
        'date_scheduled',
        'date_sent',
        'response_status',
        'call_time',
        'retries',
    )
    list_editable = (
        'response_status',
        'call_time',
        'retries',
        'parsed_message',
    )
    list_filter = (
        'type_message',
        'response_status',
    )
    search_fields = (
        'patient__first_name',
    )
    ordering = ('-date_sent', 'date_scheduled')

from rest_framework import serializers
from .models import Message, MessagingSchedule


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'order',
            'type_message',
            'message',
            'track_file',
            'date_created',
            'total_sms',
            'sms_received',
            'sms_failed',
            'total_calls',
            'calls_answered',
            'calls_failed',
            'average_call_time',
        )
        read_only_fields = (
            'date_created',
            'total_sms',
            'sms_received',
            'sms_failed',
            'total_calls',
            'calls_answered',
            'calls_failed',
            'average_call_time',
        )


class MessagingScheduleSerializer(serializers.ModelSerializer):
    retries = serializers.IntegerField(max_value=5, min_value=0)
    message_details = serializers.SerializerMethodField()
    patient_code = serializers.SerializerMethodField()

    class Meta:
        model = MessagingSchedule
        fields = (
            'id',
            'message',
            'message_details',
            'patient',
            'patient_code',
            'parsed_message',
            'type_message',
            'date_scheduled',
            'date_sent',
            'response_status',
            'call_time',
            'retries',
        )
        read_only_fields = (
            'date_sent',
        )

    def get_message_details(self, obj):
        return {
            "order": obj.message.order,
            "type_message": obj.message.type_message,
        }

    def get_patient_code(self, obj):
        return obj.patient.code

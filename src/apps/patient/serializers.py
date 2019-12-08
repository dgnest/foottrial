from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = (
            'id',
            'code',
            'first_name',
            'dni',
            'cellphone',
            'birthday',
            'is_active',
            'deactivate_reason',
            'date_joined',
            'date_deactivate',
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
        read_only_fields = (
            'date_joined',
            'sms_scheduled',
            'total_sms',
            'sms_received',
            'sms_failed',
            'calls_scheduled',
            'total_calls',
            'calls_answered',
            'calls_failed',
        )

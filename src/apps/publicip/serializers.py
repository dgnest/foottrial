from rest_framework import serializers
from .models import PublicIP


class PublicIPSerializer(serializers.ModelSerializer):
    date_updated = serializers.ReadOnlyField()

    class Meta:
        model = PublicIP
        fields = (
            'id',
            'public_ip',
            'date_updated',
        )

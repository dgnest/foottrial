from rest_framework import viewsets
from .models import PublicIP
from .serializers import PublicIPSerializer


class PublicIPViewSet(viewsets.ModelViewSet):

    queryset = PublicIP.objects.all()
    serializer_class = PublicIPSerializer
    filter_fields = (
        'public_ip',
    )
    ordering = (
        'date_updated',
    )

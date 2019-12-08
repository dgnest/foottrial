from rest_framework import viewsets
from .models import Hospital
from .serializers import HospitalSerializer


class HospitalViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_fields = (
        'name',
        'abbrev',
    )
    search_fields = (
        'name',
        'abbrev',
        'doctor',
    )

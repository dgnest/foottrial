from apps.common.mixins import LoginRequiredMixin

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import View

from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework import viewsets

from .models import Patient
from .serializers import PatientSerializer


class PatientView(LoginRequiredMixin, View):
    template_name = 'home/home.html'
    message = ''

    def get(self, request, *args, **kwargs):
        patient_id = kwargs.get('patient_id')
        if patient_id:
            get_object_or_404(Patient, pk=patient_id)
        ctx = {
            'message': self.message,
        }
        return render_to_response(
            self.template_name,
            context=ctx,
            context_instance=RequestContext(request),
        )


class PatientViewSet(viewsets.ModelViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_fields = (
        'code',
        'dni',
        'cellphone',
        'is_active',
        'hospital',
        'hospital__abbrev',
        'deactivate_reason',
    )
    ordering = (
        'code',
        'date_joined',
        'date_deactivate',
    )
    search_fields = (
        'code',
    )

    def perform_update(self, serializer):
        user = authenticate(
            username=self.request.user.email,
            password=self.request.data.get("password"),
        )
        if user:
            serializer.save()
        else:
            raise exceptions.AuthenticationFailed('Incorrect Password')

from django.conf.urls import url
from .views import PatientView


urlpatterns = [
    url(r'^ingresar/$', PatientView.as_view()),
    url(r'^pacientes/$', PatientView.as_view()),
    url(r'^pacientes/(?P<patient_id>\d+)/$', PatientView.as_view()),
    url(r'^pacientes/(?P<patient_id>\d+)/edit/$', PatientView.as_view()),
    url(r'^monitoreo/$', PatientView.as_view()),
    url(r'^monitoreo/(?P<patient_id>\d+)/$$', PatientView.as_view()),
]

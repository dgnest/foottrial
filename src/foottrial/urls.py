from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers
from rest_framework.authtoken import views

from apps.hospital.views import HospitalViewSet
from apps.patient.views import PatientViewSet
from apps.message.views import MessageViewSet, MessagingScheduleViewSet
from apps.publicip.views import PublicIPViewSet


router = routers.DefaultRouter()

# Hospital.
router.register(r'hospitals', HospitalViewSet)
# Patient.
router.register(r'patients', PatientViewSet)
# Message.
router.register(r'messages', MessageViewSet)
router.register(r'schedules', MessagingScheduleViewSet)
# PublicIP.
router.register(r'publicip', PublicIPViewSet)


urlpatterns = [
    # Admin.
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # Browsable API.
    url(r'^api/', include(router.urls)),
    url(
        r'^api-auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework'
        )
    ),
    url(r'^api-token-auth/', views.obtain_auth_token),
    # Home app.
    url(r'^', include('apps.home.urls', namespace='home_app')),
    # Patient app.
    url(r'^', include('apps.patient.urls', namespace='patient_app')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

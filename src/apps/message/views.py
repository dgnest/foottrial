from rest_framework import permissions
from rest_framework import viewsets

from .models import Message, MessagingSchedule
from .serializers import MessageSerializer, MessagingScheduleSerializer


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_fields = (
        'order',
        'type_message',
    )
    ordering = (
        'date_created',
    )
    search_fields = (
        'message',
    )


class MessagingScheduleViewSet(viewsets.ModelViewSet):

    queryset = MessagingSchedule.objects.all()
    serializer_class = MessagingScheduleSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_fields = (
        'message',
        'patient',
        'type_message',
        'response_status',
        'retries',
        'date_scheduled',
        'date_sent',
    )
    ordering = (
        'date_scheduled',
        'date_sent',
    )

    def get_queryset(self, **kwargs):
        if "exclude_response_status" in self.request.query_params.keys():
            exclude_response_status = self.request.query_params.dict().get(
                "exclude_response_status",
            )
            self.queryset = self.queryset.exclude(
                response_status=exclude_response_status,
            )
        return self.queryset

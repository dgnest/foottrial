from apps.message.models import MessagingSchedule

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


def update_message_analytics(msg_scheduled):
    message = msg_scheduled.message
    patient = msg_scheduled.patient
    if msg_scheduled.type_message == "CALL":
        patient.calls_scheduled = MessagingSchedule.objects.filter(
            type_message="CALL",
            response_status="SCHEDULED",
            patient=patient,
        ).count()
        patient.total_calls = MessagingSchedule.objects.filter(
            type_message="CALL",
            patient=patient,
        ).exclude(response_status="SCHEDULED").count()
        message.total_calls = MessagingSchedule.objects.filter(
            type_message="CALL",
            response_status="SCHEDULED",
            message=message,
        ).count()
        patient.calls_answered = MessagingSchedule.objects.filter(
            type_message="CALL",
            response_status="RECEIVED",
            patient=patient,
        ).count()
        message.calls_answered = MessagingSchedule.objects.filter(
            type_message="CALL",
            response_status="RECEIVED",
            message=message,
        ).count()
        patient.calls_failed = MessagingSchedule.objects.filter(
            type_message="CALL",
            response_status="FAILED",
            patient=patient,
        ).count()
        message.calls_failed = MessagingSchedule.objects.filter(
            type_message="CALL",
            response_status="FAILED",
            message=message,
        ).count()
        # average_call_time = MessagingSchedule.objects.filter(
        #     type_message="CALL",
        #     response_status="RECEIVED",
        #     message=message,
        # ).aggregate(Avg('call_time')).get('call_time__avg', 0.0)
        # message.average_call_time = average_call_time
    if msg_scheduled.type_message == "SMS":
        patient.sms_scheduled = MessagingSchedule.objects.filter(
            type_message="SMS",
            response_status="SCHEDULED",
            patient=patient,
        ).count()
        patient.total_sms = MessagingSchedule.objects.filter(
            type_message="SMS",
            patient=patient,
        ).exclude(response_status="SCHEDULED").count()
        message.total_sms = MessagingSchedule.objects.filter(
            type_message="SMS",
            response_status="SCHEDULED",
            message=message,
        ).count()
        patient.sms_received = MessagingSchedule.objects.filter(
            type_message="SMS",
            response_status="RECEIVED",
            patient=patient,
        ).count()
        message.sms_received = MessagingSchedule.objects.filter(
            type_message="SMS",
            response_status="RECEIVED",
            message=message,
        ).count()
        patient.sms_failed = MessagingSchedule.objects.filter(
            type_message="SMS",
            response_status="FAILED",
            patient=patient,
        ).count()
        message.sms_failed = MessagingSchedule.objects.filter(
            type_message="SMS",
            response_status="FAILED",
            message=message,
        ).count()
    patient.save()
    message.save()


@receiver(pre_save, sender=MessagingSchedule)
def update_message_analytics_signal(sender, instance=None, **kwargs):
    pre_save.disconnect(
        update_message_analytics_signal,
        sender=MessagingSchedule,
    )
    msg_scheduled = instance
    old_msg_scheduled = MessagingSchedule.objects.filter(
        pk=msg_scheduled.id,
    ).first()
    # Check if the message is being updated. It must be created.
    if old_msg_scheduled:
        if (old_msg_scheduled.response_status == "SCHEDULED" and
                msg_scheduled.response_status != "SCHEDULED"):
            msg_scheduled.date_sent = timezone.now()
            msg_scheduled.save()
        update_message_analytics(msg_scheduled)
    pre_save.connect(
        update_message_analytics_signal,
        sender=MessagingSchedule,
    )

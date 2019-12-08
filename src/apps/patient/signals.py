from apps.message.models import Message, MessagingSchedule

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Patient
from .utils import Schedule


def update_message_analytics(patient):
    # Add total messages schedules to patients.
    patient.calls_scheduled = MessagingSchedule.objects.filter(
        patient=patient,
        type_message="CALL",
    ).count()
    patient.total_calls = 0
    patient.sms_scheduled = MessagingSchedule.objects.filter(
        patient=patient,
        type_message="SMS",
    ).count()
    patient.total_sms = 0
    patient.save()
    # Add total messages schedules to individual messages.
    for message in Message.objects.all():
        message.total_calls += MessagingSchedule.objects.filter(
            message=message,
            patient=patient,
            type_message="CALL",
        ).count()
        message.total_sms += MessagingSchedule.objects.filter(
            message=message,
            patient=patient,
            type_message="SMS",
        ).count()
        message.save()


def create_messaging_schedule(patient):
    for scheduled_message in Schedule(date=timezone.now()).schedule():
        message = Message.objects.get(
            order=scheduled_message.order,
            type_message=scheduled_message.goal,
        )
        parsed_message = message.message % {
            "patient": patient.first_name,
            "doctor": patient.hospital.doctor,
            "hospital_phone": patient.hospital.phone,
        }
        MessagingSchedule.objects.create(
            message=message,
            patient=patient,
            parsed_message=parsed_message,
            type_message=scheduled_message.type_message,
            date_scheduled=scheduled_message.date,
        )
    update_message_analytics(patient)


@receiver(post_save, sender=Patient)
def schedule_messages(sender, instance=None, created=False, **kwargs):
    post_save.disconnect(schedule_messages, sender=Patient)
    pre_save.disconnect(update_patient, sender=Patient)
    patient = instance
    if created:
        create_messaging_schedule(patient)
    post_save.connect(schedule_messages, sender=Patient)
    pre_save.connect(update_patient, sender=Patient)


@receiver(pre_save, sender=Patient)
def update_patient(sender, instance=None, **kwargs):
    pre_save.disconnect(update_patient, sender=Patient)
    new_patient = instance
    old_patient = Patient.objects.filter(pk=new_patient.id).first()
    if old_patient:
        if old_patient.is_active == True and new_patient.is_active == False:
            new_patient.date_deactivate = timezone.now()
            new_patient.save()
        elif old_patient.is_active == False and new_patient.is_active == True:
            new_patient.date_deactivate = None
            new_patient.save()
    pre_save.connect(update_patient, sender=Patient)

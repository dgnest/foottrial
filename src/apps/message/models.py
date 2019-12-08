from django.db import models
from django.utils import timezone


class Message(models.Model):

    order = models.PositiveIntegerField()
    REMINDER = 'R'
    MOTIVATIONAL = 'M'
    TYPES = (
        (REMINDER, 'Recordatorio'),
        (MOTIVATIONAL, 'Motivacional'),
    )
    type_message = models.CharField(
        max_length=1,
        choices=TYPES,
        default=MOTIVATIONAL,
    )
    message = models.CharField(
        max_length=500,
    )
    track_file = models.FileField(
        max_length=500,
        upload_to='tracks',
    )
    date_created = models.DateTimeField(default=timezone.now)
    # SMS KPIs by patient.
    total_sms = models.IntegerField(default=0)
    sms_received = models.IntegerField(default=0)
    sms_failed = models.IntegerField(default=0)
    # Call KPIs by patient.
    total_calls = models.IntegerField(default=0)
    calls_answered = models.IntegerField(default=0)
    calls_failed = models.IntegerField(default=0)
    average_call_time = models.FloatField(
        default=0.0,
    )
    schedule = models.ManyToManyField(
        'patient.Patient',
        through='message.MessagingSchedule',
    )

    def __unicode__(self):
        return self.type_message + unicode(self.order)

    class Meta:
        db_table = 'message'
        unique_together = ('order', 'type_message')


class MessagingSchedule(models.Model):

    message = models.ForeignKey('message.Message')
    patient = models.ForeignKey('patient.Patient')
    parsed_message = models.CharField(
        max_length=500,
        blank=True,
    )
    CALL = 'CALL'
    SMS = 'SMS'
    TYPES = (
        (CALL, 'Llamada'),
        (SMS, 'Mensaje de Texto'),
    )
    type_message = models.CharField(
        max_length=5,
        choices=TYPES,
        default=CALL,
    )
    date_scheduled = models.DateField()
    date_sent = models.DateTimeField(
        blank=True,
        null=True,
    )
    SCHEDULED = 'SCHEDULED'
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'
    FAILED = 'FAILED'
    STATUS = (
        (SCHEDULED, 'SCHEDULED'),
        (SENT, 'SENT'),
        (RECEIVED, 'RECEIVED'),
        (FAILED, 'FAILED'),
    )
    response_status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=SCHEDULED,
    )
    call_time = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
    )
    retries = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        db_table = 'messaging_schedule'


from .signals import update_message_analytics_signal

# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Patient(models.Model):

    code = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(
                regex=r'^[\d]{1}-[\d]{3}$',
                message='Must follow the pattern "^[\d]{1}-[\d]{3}$"',
                code='invalid_code'
            ),
        ]
    )
    dni = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message='DNI must be a numeric 8 digits length',
                code='invalid_dni'
            ),
        ]
    )
    first_name = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^([^0-9]*)$',
                message='First name must be just text without numbers',
                code='invalid_dni'
            ),
        ]
    )
    cellphone = models.IntegerField(
        validators=[
            RegexValidator(
                regex=r'^\d{9}$',
                message='cellphone must be a numeric 9 digits length',
                code='invalid_cellphone'
            ),
        ]
    )
    birthday = models.DateField()
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    date_deactivate = models.DateTimeField(
        blank=True,
        null=True,
    )

    EXIT = 'E'
    ULCER = 'U'
    DIED = 'D'
    REASONS = (
        (EXIT, 'Se retiró del estudio'),
        (ULCER, 'Desarrolló una ulcera'),
        (DIED, 'Falleció'),
    )
    deactivate_reason = models.CharField(
        max_length=1,
        choices=REASONS,
        null=True,
    )

    hospital = models.ForeignKey(
        'hospital.Hospital',
        related_name='patient_set',
    )
    # SMS KPIs by patient.
    sms_scheduled = models.IntegerField(default=0)
    total_sms = models.IntegerField(default=0)
    sms_received = models.IntegerField(default=0)
    sms_failed = models.IntegerField(default=0)
    # Call KPIs by patient.
    calls_scheduled = models.IntegerField(default=0)
    total_calls = models.IntegerField(default=0)
    calls_answered = models.IntegerField(default=0)
    calls_failed = models.IntegerField(default=0)

    def __unicode__(self):
        return '-'.join([self.first_name, unicode(self.code)])

    class Meta:
        db_table = 'patient'


from .signals import schedule_messages, update_patient

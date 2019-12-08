# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('type_message', models.CharField(default=b'M', max_length=1, choices=[(b'R', b'Recordatorio'), (b'M', b'Motivacional')])),
                ('message', models.CharField(max_length=500)),
                ('track_file', models.FileField(max_length=500, upload_to=b'tracks')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_sms', models.IntegerField(default=0)),
                ('sms_received', models.IntegerField(default=0)),
                ('sms_failed', models.IntegerField(default=0)),
                ('total_calls', models.IntegerField(default=0)),
                ('calls_answered', models.IntegerField(default=0)),
                ('calls_failed', models.IntegerField(default=0)),
                ('average_call_time', models.DecimalField(default=0.0, max_digits=2, decimal_places=1)),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='MessagingSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parsed_message', models.CharField(max_length=500, blank=True)),
                ('type_message', models.CharField(default=b'CALL', max_length=5, choices=[(b'CALL', b'Llamada'), (b'SMS', b'Mensaje de Texto')])),
                ('date_scheduled', models.DateField()),
                ('date_sent', models.DateTimeField(null=True, blank=True)),
                ('response_status', models.CharField(default=b'SCHEDULED', max_length=10, choices=[(b'SCHEDULED', b'SCHEDULED'), (b'SENT', b'SENT'), (b'RECEIVED', b'RECEIVED'), (b'FAILED', b'FAILED')])),
                ('call_time', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('retries', models.PositiveIntegerField(default=0)),
                ('message', models.ForeignKey(to='message.Message')),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
            options={
                'db_table': 'messaging_schedule',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='schedule',
            field=models.ManyToManyField(to='patient.Patient', through='message.MessagingSchedule'),
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set([('order', 'type_message')]),
        ),
    ]

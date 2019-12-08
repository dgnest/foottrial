#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging
import os

import pika
import requests
from apps.message.models import MessagingSchedule
from apps.publicip.models import PublicIP
from django.conf import settings
from django.utils import timezone
from django_slack import slack_message
from foottrial.celery import app

logger = logging.getLogger('foottrial')


def send_message(message):
    try:
        params = pika.URLParameters(settings.BROKER_URL)
        params.socket_timeout = 5
        connection = pika.BlockingConnection(params)
        channel_connection = connection.channel()
        channel_connection.exchange_declare(
            exchange=settings.QUEUE_EXCHANGE,
            exchange_type='direct',
            passive=False,
            durable=True,
            auto_delete=False
        )

        channel_connection.queue_declare(
            queue=settings.QUEUE_NAME,
            auto_delete=True
        )

        channel_connection.queue_bind(
            queue=settings.QUEUE_NAME,
            exchange=settings.QUEUE_EXCHANGE,
            routing_key=settings.QUEUE_KEY,
        )
        channel_connection.basic_publish(
            exchange=settings.QUEUE_EXCHANGE,
            routing_key=settings.QUEUE_KEY,
            body=json.dumps(message),
            properties=pika.BasicProperties(content_type='application/json')
        )

        connection.close()
        return True
    except json.JSONEncodeError:
        logger.error(
            'Error decode data',
            exc_info=True,
            extra=message,
        )


@app.task(name='make-message-request')
def make_message_request(scheduled_message):
    print('make_message_request')
    # SMS and call services.
    SLAVE_IP = 'http://' + PublicIP.objects.first().public_ip
    CALL_URL = SLAVE_IP + os.getenv('CALL_URL', '/call/')
    SMS_URL = SLAVE_IP + os.getenv('SMS_URL', '/sms/')

    type_message = scheduled_message.type_message

    if type_message == 'CALL':
        payload = {
            'id': scheduled_message.id,
            'message_id': scheduled_message.message.id,
            'cellphone': scheduled_message.patient.cellphone,
        }
        response = requests.post(
            CALL_URL,
            data=json.dumps(payload),
        )
        print(response)
        print(response.json())
        print('CALL sent: %s' % str(scheduled_message.id))
        # Update call status.
        scheduled_message.response_status = response.json().get('status')
        scheduled_message.save()
    elif type_message == 'SMS':
        payload = {
            'id': scheduled_message.id,
            'message': scheduled_message.parsed_message.encode('utf8'),
            'cellphone': scheduled_message.patient.cellphone,
        }
        response = requests.post(
            SMS_URL,
            data=json.dumps(payload),
        )
        print(response)
        print(response.json())
        print('SMS sent: %s' % str(scheduled_message.id))
        # Update sms status.
        scheduled_message.response_status = response.json().get('status')
        scheduled_message.save()
    else:
        print('Message Failed', type_message)


@app.task
def send_scheduled_messages():
    now = timezone.now().date()
    slack_message('slack/info_proccess.slack', {
        'proccess': {
            'name': 'send_scheduled_messages',
            'state': 'Start',
            'date': now,
        },
    })
    messages = MessagingSchedule.objects.filter(
        date_scheduled=now,
        patient__is_active=True,
        response_status='SCHEDULED',
    )
    for message in messages:
        type_message = message.type_message
        body = {
            'resource': type_message.lower(),
            'id': message.id,
            'cellphone': message.patient.cellphone,
        }

        if type_message == 'CALL':
            body['message_id'] = message.message.id
        else:
            body['message'] = message.parsed_message.encode('utf8')

        print('body: {}'.format(body))
        slack_message('slack/message.slack', {
            'message': body,
        })
        is_sending = send_message(body)
        if is_sending:
            MessagingSchedule.objects.filter(pk=message.id).update(**{
                'response_status': 'SENT',
            })
    slack_message('slack/info_proccess.slack', {
        'proccess': {
            'name': 'send_scheduled_messages',
            'state': 'Finished',
            'date': now,
        },
    })
    print('Message of the day were sent')

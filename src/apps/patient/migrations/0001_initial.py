# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=5, validators=[django.core.validators.RegexValidator(regex=b'^[\\d]{1}-[\\d]{3}$', message=b'Must follow the pattern "^[\\d]{1}-[\\d]{3}$"', code=b'invalid_code')])),
                ('dni', models.CharField(unique=True, max_length=8, validators=[django.core.validators.RegexValidator(regex=b'^\\d{8}$', message=b'DNI must be a numeric 8 digits length', code=b'invalid_dni')])),
                ('first_name', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex=b'^([^0-9]*)$', message=b'First name must be just text without numbers', code=b'invalid_dni')])),
                ('cellphone', models.IntegerField(unique=True, validators=[django.core.validators.RegexValidator(regex=b'^\\d{9}$', message=b'cellphone must be a numeric 9 digits length', code=b'invalid_cellphone')])),
                ('birthday', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_deactivate', models.DateTimeField(null=True, blank=True)),
                ('deactivate_reason', models.CharField(max_length=1, null=True, choices=[(b'E', b'Se retir\xc3\xb3 del estudio'), (b'U', b'Desarroll\xc3\xb3 una ulcera'), (b'D', b'Falleci\xc3\xb3')])),
                ('sms_scheduled', models.IntegerField(default=0)),
                ('total_sms', models.IntegerField(default=0)),
                ('sms_received', models.IntegerField(default=0)),
                ('sms_failed', models.IntegerField(default=0)),
                ('calls_scheduled', models.IntegerField(default=0)),
                ('total_calls', models.IntegerField(default=0)),
                ('calls_answered', models.IntegerField(default=0)),
                ('calls_failed', models.IntegerField(default=0)),
                ('hospital', models.ForeignKey(related_name='patient_set', to='hospital.Hospital')),
            ],
            options={
                'db_table': 'patient',
            },
        ),
    ]

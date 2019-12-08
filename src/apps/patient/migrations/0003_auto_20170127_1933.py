# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_auto_20170127_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='cellphone',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator(regex=b'^\\d{9}$', message=b'cellphone must be a numeric 9 digits length', code=b'invalid_cellphone')]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='dni',
            field=models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(regex=b'^\\d{8}$', message=b'DNI must be a numeric 8 digits length', code=b'invalid_dni')]),
        ),
    ]

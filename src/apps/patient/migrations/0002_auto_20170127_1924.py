# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='code',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(regex=b'^[\\d]{1}-[\\d]{3}$', message=b'Must follow the pattern "^[\\d]{1}-[\\d]{3}$"', code=b'invalid_code')]),
        ),
    ]

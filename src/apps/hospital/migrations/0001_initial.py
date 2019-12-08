# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('abbrev', models.CharField(max_length=20, blank=True)),
                ('doctor', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'hospital',
            },
        ),
    ]

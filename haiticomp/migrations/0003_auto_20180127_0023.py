# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haiticomp', '0002_auto_20180126_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='comppackage',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comppackage',
            name='is_wrong',
            field=models.BooleanField(default=False),
        ),
    ]

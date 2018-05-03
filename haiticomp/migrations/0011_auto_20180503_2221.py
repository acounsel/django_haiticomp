# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-03 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haiticomp', '0010_comppackagerevision_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comppackage',
            name='land_area',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='comppackagerevision',
            name='land_area',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
    ]

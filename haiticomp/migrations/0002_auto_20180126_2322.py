# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-26 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haiticomp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('lost_harvest', 'Lost Harvest'), ('food_security', 'Food Security'), ('improvements', 'Improvements'), ('final_compensation', 'Final Compensation')], max_length=180),
        ),
    ]

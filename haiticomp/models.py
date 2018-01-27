# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CompPackage(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField(blank=True, null=True)
    tax_id = models.CharField(max_length=200)
    land_area = models.DecimalField(max_digits=4, decimal_places=2)
    num_family = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_wrong = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def group_payments_by_date(self):
        payment_dict = {}
        payments = self.payment_set.order_by('date')
        for payment in payments:
            if payment.date in payment_dict:
                payment_dict[payment.date].append(payment)
            else:
                payment_dict[payment.date] = [payment,]
        return payment_dict

class Payment(models.Model):
    LOST_HARVEST = 'lost_harvest'
    FOOD_SECURITY = 'food_security'
    IMPROVEMENTS = 'improvements'
    FINAL_COMPENSATION = 'final_compensation'
    PAYMENT_TYPE_CHOICES = (
        (LOST_HARVEST, 'Lost Harvest'),
        (FOOD_SECURITY, 'Food Security'),
        (IMPROVEMENTS, 'Improvements'),
        (FINAL_COMPENSATION, 'Final Compensation'),
    )
    value = models.IntegerField()
    date = models.DateField()
    payment_type = models.CharField(max_length=180, choices=PAYMENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_paid = models.BooleanField(default=True)
    package = models.ForeignKey(CompPackage)

    def __str__(self):
        return '$%s payment to %s' % (self.value, self.package.name)





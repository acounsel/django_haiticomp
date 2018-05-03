# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
from decimal import Decimal
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CompPackage(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    tax_id = models.CharField(max_length=200, blank=True)
    land_area = models.DecimalField(max_digits=6, decimal_places=3)
    num_family = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_wrong = models.BooleanField(default=False)
    issue = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('update-compensation', kwargs={'pk': self.id})

    def get_recurring_payments(self):
        return ['lost_harvest', 'food_security']

    def group_payments_by_date(self):
        payment_dict = OrderedDict()
        payments = self.payment_set.order_by('date')
        for payment in payments:
            if payment.date.year in payment_dict:
                payment_dict[payment.date.year]['payments'].append(payment)
            else:
                payment_dict[payment.date.year] = {
                    'payments': [payment,],
                }
        for key, value in payment_dict.iteritems():
            total = 0
            gourde_total = 0
            for payment in value['payments']:
                total += payment.value
                gourde_total += payment.convert_to_gourdes()
            value['total'] = (total, gourde_total)
        return payment_dict

    def get_payment_value(self, payment_type):
        if payment_type == Payment.LOST_HARVEST:
            value = self.get_loss_of_harvest_compensation()
        elif payment_type == Payment.FOOD_SECURITY:
            value = self.get_num_family_compensation()
        elif payment_type == Payment.FINAL_COMPENSATION:
            value = self.get_final_compensation()
        return value

    def get_loss_of_harvest_compensation(self):
        comp = 1450 * self.land_area
        return comp

    def get_num_family_compensation(self):
        comp = 80 * self.num_family
        return comp

    def get_final_compensation(self):
        comp = 1450 * self.land_area * 5 * Decimal(1.1725)
        return round(comp, 2)

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
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_type = models.CharField(max_length=180, choices=PAYMENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_paid = models.BooleanField(default=True)
    package = models.ForeignKey(CompPackage)

    def __str__(self):
        return '$%s payment to %s' % (self.value, self.package.name)

    def convert_to_gourdes(self):
        if self.date.year < 2013:
            return self.value * 40
        else: 
            return int(self.value * Decimal(43.5))


class CompPackageRevision(models.Model):
    package = models.ForeignKey(CompPackage)
    land_area = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    num_family = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return '%s Revision %s' % (self.package.name, self.timestamp)

    @receiver(post_save, sender=CompPackage)
    def create_revision(sender, instance, created, **kwargs):
            CompPackageRevision.objects.create(
                package=instance,
                land_area=instance.land_area,
                num_family=instance.num_family,
                age=instance.age,
            )


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from haiticomp.models import Payment, CompPackage
# Register your models here.

admin.site.register(Payment)
admin.site.register(CompPackage)

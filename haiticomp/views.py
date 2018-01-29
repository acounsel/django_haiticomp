# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect

from haiticomp.models import Payment, CompPackage
# Create your views here.
def index(request):
    return redirect(reverse('farmer-input', kwargs={'language': 'kreyol'}))

def view_compensation(request, package_id=None, language='kreyol'):
    if language == 'english':
        template = 'package.html'
    else:
        template = 'kreyol/package.html'
    package = CompPackage.objects.get(id=package_id)
    payment_dict = package.group_payments_by_date()
    data = {
        'package': package,
        'payment_dict': payment_dict,
        'language': language,
    }

    return render(request, template, data)

def farmer_input(request, language='kreyol'):
    if language == 'english':
        template = 'farmer_input.html'
    else:
        template = 'kreyol/farmer_input.html'
    error_message = ''
    if request.method=='POST':
        tax_id = request.POST['tax_id']
        tax_id_digits = ''.join([i for i in tax_id if i.isdigit()])
        try:
            package = CompPackage.objects.get(tax_id=tax_id_digits)
            return redirect(reverse('package', kwargs={'package_id': package.id, 'language':language}))
        except CompPackage.DoesNotExist:
            error_message = 'No Compensation For ID Number: %s' % tax_id

    data = {
        'error_message': error_message,
        'language': language,
    }
    return render(request, template, data)

def verify_compensation(request, package_id, language='kreyol'):
    if language == 'english':
        template = 'response_recorded.html'
    else:
        template = 'kreyol/response_recorded.html'
    package = CompPackage.objects.get(id=package_id)
    package.is_verified = True
    package.save()
    data = {
        'package': package,
        'language': language,
    }
    return render(request, template, data)

def wrong_compensation(request, package_id, language='kreyol'): 
    if language == 'english':
        template = 'response_recorded.html'
    else: 
        template = 'kreyol/response_recorded.html'
    package = CompPackage.objects.get(id=package_id)
    package.is_wrong = True
    package.save()
    data = {
        'package': package,
        'language': language,
    }
    return render(request, template, data)

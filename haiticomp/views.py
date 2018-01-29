# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from haiticomp.models import Payment, CompPackage

def index(request):
    return redirect(reverse('farmer-input', kwargs={'language': 'kreyol'}))

class BaseView(View):

    def gather_data(self, request, language='kreyol'):
        if language == 'english':
            other_language = 'kreyol'
        else:
            other_language = 'english'
        data = {
            'language': language,
            'other_language': other_language,
        }
        return data

class ViewCompensation(BaseView):

    def get(self, request, package_id, language):
        template = '%s/package.html' % language
        data = self.gather_data(request, language)
        package = CompPackage.objects.get(id=package_id)
        payment_dict = package.group_payments_by_date()
        data.update({
            'package': package,
            'payment_dict': payment_dict,
        })
        return render(request, template, data)

class FarmerInput(BaseView):

    def get(self, request, language):
        data = self.gather_data(request, language)
        template = '%s/farmer_input.html' % language
        return render(request, template, data)

    def post(self, request, language):
        data = self.gather_data(request, language)
        template = '%s/farmer_input.html' % language
        error_message = ''
        if request.method=='POST':
            tax_id = request.POST['tax_id']
            tax_id_digits = ''.join([i for i in tax_id if i.isdigit()])
            try:
                package = CompPackage.objects.get(tax_id=tax_id_digits)
                return redirect(reverse('package', kwargs={'package_id': package.id, 'language':language}))
            except CompPackage.DoesNotExist:
                error_message = 'No Compensation For ID Number: %s' % tax_id
        data.update({
            'error_message': error_message,
        })
        return render(request, template, data)

class VerifyCompensation(BaseView):

    def get(self, request, package_id, language):
        template = '%s/response_recorded.html' % language
        data = self.gather_data(request, language)
        package = CompPackage.objects.get(id=package_id)
        package.is_verified = True
        package.save()
        data.update({
            'package': package,
        })
        return render(request, template, data)

class WrongCompensation(BaseView):

    def get(self, request, package_id, language):
        template = '%s/response_recorded.html' % language
        data = self.gather_data(request, language)
        package = CompPackage.objects.get(id=package_id)
        package.is_wrong = True
        package.save()
        data.update({
            'package': package,
        })
        return render(request, template, data)

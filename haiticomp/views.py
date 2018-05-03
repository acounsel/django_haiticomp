# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView 

from haiticomp.models import Payment, CompPackage
from haiticomp.forms import CompPackageForm

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

# View Compensation views
class ViewCompensation(BaseView):

    def get(self, request, package_id, language=None):
        if not language:
            language='kreyol'
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
        template = '%s/report_issue.html' % language
        data = self.gather_data(request, language)
        package = CompPackage.objects.get(id=package_id)
        package.is_wrong = True
        package.save()
        data.update({
            'package': package,
        })
        return render(request, template, data)

    def post(self, request, package_id, language):
        template = '%s/response_recorded.html' % language
        data = self.gather_data(request, language)
        package = CompPackage.objects.get(id=package_id)
        issue = request.POST['issue']
        package.issue = issue
        package.save()
        data.update({
            'package': package,
        })
        return render(request, template, data)

class EditCompensation(View):
    model = CompPackage
    form_class = CompPackageForm

    def create_annual_payments(self, comp_package):
        years = (2011, 2012, 2013)
        for year in years:
            for payment_type in comp_package.get_recurring_payments():
                payment = self.create_payment(comp_package, year, payment_type)
        payment = self.create_payment(comp_package, 2013, Payment.FINAL_COMPENSATION)
        return True

    def create_payment(self, comp_package, year, payment_type):
        payment = Payment.objects.create(
            package=comp_package,
            date=datetime.date(year, 1, 1),
            payment_type=payment_type,
            value=comp_package.get_payment_value(payment_type)
        )
        return payment

class CreateCompensation(EditCompensation, CreateView):

    def form_valid(self, form):
        response = super(CreateCompensation, self).form_valid(form)
        comp_package = form.instance
        self.create_annual_payments(comp_package)
        return response

class UpdateCompensation(EditCompensation, UpdateView):
    template_name = 'kreyol/package.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateCompensation, self).get_context_data()
        context['payment_dict'] = context['comppackage'].group_payments_by_date()
        return context

    def form_valid(self, form):
        if 'name' in form.changed_data:
            form.instance.pk = None
        response = super(UpdateCompensation, self).form_valid(form)
        form.instance.payment_set.all().delete()
        self.create_annual_payments(form.instance)
        
        return response

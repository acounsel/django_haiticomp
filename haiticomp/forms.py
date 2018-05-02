from django import forms
from django.forms import ModelForm

from haiticomp.models import CompPackage

class CompPackageForm(ModelForm):

    class Meta(object):
        model = CompPackage
        fields = ('name', 'age', 'land_area', 'num_family')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sipote Destine'}),
            'age': forms.TextInput(attrs={'class':'form-control', 'placeholder':'20'}),
            'num_family': forms.TextInput(attrs={'class':'form-control text-danger', 'placeholder':'6'}),
            'land_area': forms.TextInput(attrs={'class':'form-control text-primary', 'placeholder':'0.50'})
        }
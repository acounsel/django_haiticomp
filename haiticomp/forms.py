from django import forms
from django.forms import ModelForm

from haiticomp.models import CompPackage

class CompPackageForm(ModelForm):

    class Meta(object):
        model = CompPackage
        fields = ('name', 'age', 'land_area', 'num_family')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Josef Alians'}),
            'age': forms.TextInput(attrs={'class':'form-control font-weight-bold', 'placeholder':'20'}),
            'num_family': forms.TextInput(attrs={'class':'form-control text-danger font-weight-bold', 'placeholder':'10'}),
            'land_area': forms.TextInput(attrs={'class':'form-control text-primary font-weight-bold', 'placeholder':'0.50'})
        }
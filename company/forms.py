from django import forms
from .models import Company, Employer

class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)

class UpdateEmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ('user',)
 
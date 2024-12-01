from django import forms
from company.models import Company

class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)
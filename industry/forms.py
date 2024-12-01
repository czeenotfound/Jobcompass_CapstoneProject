from django import forms
from .models import Industry

class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = '__all__'
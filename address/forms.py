from django import forms
from .models import Address

class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'company',)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country','countrypostal', 'region', 'city', 'street']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'countrypostal': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
        }
from django import forms
from .models import Address

class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'company',)
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'countrypostal', 'region', 'city', 'street']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-select', 'id': 'country'}),
            'countrypostal': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'id': 'region'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
        }
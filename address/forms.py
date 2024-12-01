from django import forms
from .models import Address

class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'company',)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['region', 'province', 'city', 'barangay', 'street']
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
        }
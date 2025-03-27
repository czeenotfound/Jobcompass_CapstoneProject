from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User

from django.contrib.auth.forms import SetPasswordForm

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone', 'first_name', 'last_name', 'password1', 'password2', 'role']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email
    

class UpdateAvatarPhoneForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'phone', 'first_name', 'last_name']

        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}), 
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }



class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'otp-input',
            'maxlength': '6',
            'pattern': '[0-9]{6}',
            'inputmode': 'numeric',
            'placeholder': 'Enter 6-digit OTP',
        })
    )
    
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))


class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    new_password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))
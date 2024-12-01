from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User

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
        fields = ['avatar', 'phone']

        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
from django import forms
from .models import Job, Job_Responsibilities, Job_Experience, Application, ApplicationStatus,RequiredSkill, JobFair
from django.forms import inlineformset_factory
from address.models import Address

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'company', 'industry', 'posted_date', 'posted_time')

class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'company', 'industry', 'posted_date', 'posted_time')


class RequiredSkillForm(forms.ModelForm):
    class Meta:
        model = RequiredSkill
        fields = ['skill_name']
        widgets = {
            'skill_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '• Skill (e.g., Python, React, Project Management)'
            })
        }

class JobResponsibilitiesForm(forms.ModelForm):
    class Meta:
        model = Job_Responsibilities
        fields = ['res_name'] 
        widgets = {
            'res_name': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '• Key Responsibility (e.g., Develop web applications)',
            })
        }

class JobExperienceForm(forms.ModelForm):
    class Meta:
        model = Job_Experience
        fields = ['exp_name', 'exp_years', 'exp_description']
        widgets = {
            'exp_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title (e.g., Software Developer)',
            }),
            'exp_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '• Number of Years',
            }),
            'exp_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '• Experience description (e.g., Worked with Python and Django)',
                'rows': 4,
            }),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ('submit_date',)

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = ApplicationStatus
        fields = ['status', 'feedback']



# JOB FAIR

class CreateJobFairForm(forms.ModelForm):
    class Meta:
        model = JobFair
        exclude = ('user', 'company', 'industry',)

class UpdateJobFairForm(forms.ModelForm):
    class Meta:
        model = JobFair
        exclude = ('user', 'company', 'industry')
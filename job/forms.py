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

class JobResponsibilitiesForm(forms.ModelForm):
    class Meta:
        model = Job_Responsibilities
        fields = ['res_name']

class JobExperienceForm(forms.ModelForm):
    class Meta:
        model = Job_Experience
        fields = ['exp_name', 'exp_years', 'exp_description']

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
        exclude = ('user', 'company', 'industry', )

class UpdateJobFairForm(forms.ModelForm):
    class Meta:
        model = JobFair
        exclude = ('user', 'company', 'industry', 'is_featured', 'is_active')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),  # Use FileInput instead of ClearableFileInput
        }
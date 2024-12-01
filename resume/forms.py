from django import forms
from .models import Resume, Skill, Education, Experience, Certification, Project, SocialLink
from address.models import Address

class UpdateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user',)

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'graduation_year']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'url']

class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']
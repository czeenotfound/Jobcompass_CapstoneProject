from django import forms
from .models import Resume, Skill, Education, Experience, Certification, Project, SocialLink
from address.models import Address
from datetime import date

today = date.today().isoformat() 

class UpdateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user',)

    def clean(self):
        cleaned_data = super().clean()
        salary_type = cleaned_data.get("salary_display_type")
        fixed_salary = cleaned_data.get("expt_salary_fixed")
        min_salary = cleaned_data.get("expt_salary_min")
        max_salary = cleaned_data.get("expt_salary_max")
        salary_mode = cleaned_data.get("expt_salary_mode")

        # Ensure a salary mode is selected if salary is displayed
        if salary_type in ["fixed", "range"] and not salary_mode:
            self.add_error("expt_salary_mode", "Please select a salary mode (Hourly, Daily, etc.).")

        if salary_type == "fixed":
            if not fixed_salary:
                self.add_error("expt_salary_fixed", "Fixed salary must be provided.")
            cleaned_data["expt_salary_min"] = None
            cleaned_data["expt_salary_max"] = None

        elif salary_type == "range":
            if not (min_salary and max_salary):
                self.add_error("expt_salary_min", "Both min and max salaries are required.")
                self.add_error("expt_salary_max", "Both min and max salaries are required.")
            elif min_salary > max_salary:
                self.add_error("expt_salary_min", "Minimum salary cannot be greater than maximum salary.")
                self.add_error("expt_salary_max", "Maximum salary cannot be less than minimum salary.")
            cleaned_data["expt_salary_fixed"] = None

        else:  # Hidden salary type
            cleaned_data["expt_salary_fixed"] = None
            cleaned_data["expt_salary_min"] = None
            cleaned_data["expt_salary_max"] = None
            cleaned_data["expt_salary_mode"] = None

        return cleaned_data

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '• Skill (e.g., Python, React, Project Management)'
            })
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'graduation_year']
        widgets = {
            'degree': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Degree (e.g., High School Graduate, Bachelor of Arts in Psychology)',
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Institution (e.g., XYZ High School, ABC University)',
            }),
            'graduation_year': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Graduation Year (e.g., 2023)',
                'min': 1900,
                'max': 2100,
            }),
        }
        
        
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Job Title (e.g., Software Developer)',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Company Name (e.g., Google)',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'date',
                'max': today,
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'date',
                'max': today,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Job Description (e.g., Developed scalable web applications)',
                'rows': 4,
            }),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Certification Name (e.g., AWS Certified Solutions Architect)',
            }),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Project Title (e.g., Personal Portfolio Website)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Project Description (e.g., A personal portfolio showcasing skills)',
                'rows': 4,
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Project URL (e.g., https://github.com/yourproject)',
            }),
        }

class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']
        widgets = {
            'platform': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Platform (e.g., LinkedIn, GitHub)',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Social URL (e.g., https://linkedin.com/in/username)',
            }),
        }
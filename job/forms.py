from django import forms
from .models import Job, Job_Responsibilities, Job_IdealCandidates, Job_Benefits, Job_Experience, Job_Education, Application, ApplicationStatus, RequiredSkill, Interview, Offer, Feedback, JobFair
from skill.models import Skill as GlobalSkill
from django.utils.timezone import now

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'company', 'industry', 'posted_date', 'posted_time')

class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'company', 'industry', 'posted_date', 'posted_time')

        
    def clean(self):
        cleaned_data = super().clean()
        salary_type = cleaned_data.get("salary_display_type")
        fixed_salary = cleaned_data.get("salary_fixed")
        min_salary = cleaned_data.get("salary_min")
        max_salary = cleaned_data.get("salary_max")
        salary_mode = cleaned_data.get("salary_mode")

        # Ensure a salary mode is selected if salary is displayed
        if salary_type in ["fixed", "range"] and not salary_mode:
            self.add_error("salary_mode", "Please select a salary mode (Hourly, Daily, etc.).")

        if salary_type == "fixed":
            if not fixed_salary:
                self.add_error("salary_fixed", "Fixed salary must be provided.")
            cleaned_data["salary_min"] = None
            cleaned_data["salary_max"] = None

        elif salary_type == "range":
            if not (min_salary and max_salary):
                self.add_error("salary_min", "Both min and max salaries are required.")
                self.add_error("salary_max", "Both min and max salaries are required.")
            elif min_salary > max_salary:
                self.add_error("salary_min", "Minimum salary cannot be greater than maximum salary.")
                self.add_error("salary_max", "Maximum salary cannot be less than minimum salary.")
            cleaned_data["salary_fixed"] = None

        else:  # Hidden salary type
            cleaned_data["salary_fixed"] = None
            cleaned_data["salary_min"] = None
            cleaned_data["salary_max"] = None
            cleaned_data["salary_mode"] = None

        return cleaned_data

class RequiredSkillForm(forms.ModelForm):
    class Meta:
        model = RequiredSkill
        fields = ['skill_name']

    def clean_name(self):
        skill_name = self.cleaned_data['skill_name'].strip()

        skill, created = GlobalSkill.objects.get_or_create(
            name=skill_name, 
            defaults={'is_validated': False}
        )

        return skill.name 

class JobResponsibilitiesForm(forms.ModelForm):
    class Meta:
        model = Job_Responsibilities
        fields = ['res_name'] 
        widgets = {
            'res_name': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'rows': 2,
                'placeholder': '• Key Responsibility (e.g., Develop web applications)',
            })
        }

class JobIdealCandidatesForm(forms.ModelForm):
    class Meta:
        model = Job_IdealCandidates
        fields = ['ideal_name'] 
        widgets = {
            'ideal_name': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'rows': 2,
                'placeholder': '• Ideal Candidate (e.g., Strong problem-solving skills)',
            })
        }

class JobBenefitsForm(forms.ModelForm):
    class Meta:
        model = Job_Benefits
        fields = ['bene_name'] 
        widgets = {
            'bene_name': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'rows': 2,
                'placeholder': '• Job Benefit (e.g., Health insurance)',
            })
        }


class JobExperienceForm(forms.ModelForm):
    class Meta:
        model = Job_Experience
        fields = ['exp_type', 'exp_name', 'exp_years', 'min_exp_years', 'max_exp_years', 'exp_description']
        widgets = {
            'exp_type': forms.Select(attrs={
                'class': 'form-select mb-2',
                'placeholder': 'Experience Type',
            }),
            'exp_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Job Title (e.g., Software Developer)',
            }),
            'exp_years': forms.NumberInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Exact Years',
            }),
            'min_exp_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum Years',
            }),
            'max_exp_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum Years',
            }),
            'exp_description': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'placeholder': '• Experience description (e.g., Worked with Python and Django)',
                'rows': 4,
            }),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        exp_type = cleaned_data.get("exp_type")
        exp_years = cleaned_data.get("exp_years")
        min_exp_years = cleaned_data.get("min_exp_years")
        max_exp_years = cleaned_data.get("max_exp_years")

        errors = {}

        if exp_type == "fixed":
            if not exp_years:
                errors["exp_years"] = "Please provide a fixed number of years."
            cleaned_data["min_exp_years"] = None
            cleaned_data["max_exp_years"] = None

        elif exp_type == "range":
            if not (min_exp_years and max_exp_years):
                errors["min_exp_years"] = "Both min and max years are required for a range."
                errors["max_exp_years"] = "Both min and max years are required for a range."
            elif min_exp_years > max_exp_years:
                errors["min_exp_years"] = "Minimum experience cannot be greater than maximum experience."
                errors["max_exp_years"] = "Maximum experience cannot be less than minimum experience."
            cleaned_data["exp_years"] = None

        # Instead of blocking submission, raise errors only if ALL fields are empty
        if errors and not (exp_years or min_exp_years or max_exp_years):
            raise forms.ValidationError(errors)

        return cleaned_data


class JobEducationForm(forms.ModelForm):
    
    class Meta:
        model = Job_Education
        fields = ['education_level', 'degree']
        widgets = {
            'education_level': forms.Select(attrs={
                'class': 'form-select mb-2',
                'placeholder': 'Education Level',
            }),
            'degree': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'e.g., Bachelor of.., Diploma, etc',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['education_level'].choices = [('', 'Select Education Level')] + list(self.fields['education_level'].choices)
        

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ('submit_date',)

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = ApplicationStatus
        fields = ['status', 'feedback']


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'interview_type', 'interviewer', 'notes']
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notes'}),
        }

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['salary_display_type', 'currency', 'salary_fixed', 'salary_min', 'salary_max', 
                 'salary_mode','notes', 'benefits', 'offer_date', 'expiration_date']
        widgets = {
            'offer_date': forms.DateInput(attrs={'type': 'date', 'min': now().date().isoformat()}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'benefits': forms.Textarea(attrs={'rows': 3}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }


# JOB FAIR

class CreateJobFairForm(forms.ModelForm):
    class Meta:
        model = JobFair
        exclude = ('user', 'company', 'industry',)

class UpdateJobFairForm(forms.ModelForm):
    class Meta:
        model = JobFair
        exclude = ('user', 'company', 'industry')
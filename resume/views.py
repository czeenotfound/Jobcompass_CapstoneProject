from django.shortcuts import render, redirect
from django.forms import inlineformset_factory, BaseInlineFormSet
from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Resume,Skill, Education, Experience, Certification,Project, SocialLink
from django.forms import formset_factory
from .forms import UpdateResumeForm
from address.forms import AddressForm
from users.models import User
from users.forms import UpdateAvatarPhoneForm
from django.http import JsonResponse

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

class SkillFormSet(BaseInlineFormSet):
    def clean(self):
        # Ensure at least one skill is added
        super().clean()
        skills = [form.cleaned_data.get('name') for form in self.forms if form.cleaned_data.get('name')]
        
        if not skills:
            raise ValidationError("Please add at least one required skill.")

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'graduation_year']
        widgets = {
            'degree': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Degree (e.g., High School Graduate, Bachelor of Arts in Psychology)',
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Institution (e.g., XYZ High School, ABC University)',
            }),
            'graduation_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Graduation Year (e.g., 2023)',
                'min': 1900,
                'max': 2100,
            }),
        }
        

class EducationFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if not any(form.cleaned_data.get('degree') for form in self.forms if form.cleaned_data):
            raise ValidationError("Please add at least one education entry.")

        for form in self.forms:
            if form.cleaned_data and form.cleaned_data.get('graduation_year'):
                graduation_year = form.cleaned_data['graduation_year']
                if graduation_year < 1900 or graduation_year > 2100:
                    raise ValidationError("Graduation year must be between 1900 and 2100.")
        
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title (e.g., Software Developer)',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name (e.g., Google)',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Job Description (e.g., Developed scalable web applications)',
                'rows': 4,
            }),
        }

class ExperienceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            # Skip forms marked for deletion
            if form.cleaned_data.get('DELETE', False):
                continue

            # Check that all fields in a form are filled if the form is not empty
            if form.cleaned_data and not all(
                form.cleaned_data.get(field) for field in ['title', 'company', 'start_date', 'end_date', 'description']
            ):
                raise ValidationError("Please fill in all fields for each job experience entry.")

        
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certification Name (e.g., AWS Certified Solutions Architect)',
            }),
        }

class CertificationFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # No specific validation since certifications are optional
        pass


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Title (e.g., Personal Portfolio Website)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Project Description (e.g., A personal portfolio showcasing skills)',
                'rows': 4,
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project URL (e.g., https://github.com/yourproject)',
            }),
        }

class ProjectFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # No specific validation since projects are optional
        pass


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']
        widgets = {
            'platform': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Platform (e.g., LinkedIn, GitHub)',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Social URL (e.g., https://linkedin.com/in/username)',
            }),
        }

class SocialLinkFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass



def create_resume(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_applicant:
        resume, created = Resume.objects.get_or_create(user=request.user)
        address = resume.address if resume.address else None
        user = request.user

        # Define formsets
        ResumeSkillFormSet = inlineformset_factory(
            Resume,
            Skill, 
            form=SkillForm, 
            formset=SkillFormSet, 
            extra=3, 
            can_delete=True
        )
        ResumeEducationFormSet = inlineformset_factory(
            Resume, 
            Education, 
            form=EducationForm, 
            formset=EducationFormSet, 
            extra=1, 
            can_delete=True
        )
        ResumeExperienceFormSet = inlineformset_factory(
            Resume, Experience, 
            form=ExperienceForm, 
            formset=ExperienceFormSet, 
            extra=1, 
            can_delete=True
        )
        ResumeCertificationFormSet = inlineformset_factory(
            Resume, Certification, 
            form=CertificationForm, 
            formset=CertificationFormSet, 
            extra=1, 
            can_delete=True
        )
        ResumeProjectFormSet = inlineformset_factory(
            Resume, Project, 
            form=ProjectForm, 
            formset=ProjectFormSet, 
            extra=1, 
            can_delete=True
        )
        ResumeSocialLinkFormSet = inlineformset_factory(
            Resume, SocialLink, 
            form=SocialLinkForm, 
            formset=SocialLinkFormSet, 
            extra=1, 
            can_delete=True
        )

        form_errors = []  # Initialize once

        if request.method == 'POST':
            form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
            address_form = AddressForm(request.POST, instance=address)
            avatar_phone_form = UpdateAvatarPhoneForm(request.POST, request.FILES, instance=user)
            skill_formset = ResumeSkillFormSet(request.POST, prefix='skills', instance=resume)
            education_formset = ResumeEducationFormSet(request.POST, prefix='education', instance=resume)
            experience_formset = ResumeExperienceFormSet(request.POST, prefix='experience', instance=resume)
            certification_formset = ResumeCertificationFormSet(request.POST, prefix='certification', instance=resume)
            project_formset = ResumeProjectFormSet(request.POST, prefix='project', instance=resume)
            sociallink_formset = ResumeSocialLinkFormSet(request.POST, prefix='social_link', instance=resume)

            if form.is_valid() and address_form.is_valid() and avatar_phone_form.is_valid() and skill_formset.is_valid() and education_formset.is_valid() and experience_formset.is_valid() and certification_formset.is_valid() and project_formset.is_valid() and sociallink_formset.is_valid():
                # Save all forms and formsets
                resume_instance = form.save(commit=False)
                user.has_resume = True
                user.save()
                
                # Save the address
                address_instance = address_form.save(commit=False)
                address_instance.user = user
                address_instance.save()
                resume_instance.address = address_instance
                resume_instance.save()

                avatar_phone_form.save()
                skill_formset.save()
                education_formset.save()
                experience_formset.save()
                certification_formset.save()
                project_formset.save()
                sociallink_formset.save()

                messages.info(request, 'Your resume is now active. You can start applying for jobs.')
                return redirect('applicant-profile', pk=user.pk)  # Redirect to dashboard after success
            else:
                # Append field errors
                form_errors.extend(form.errors.values())
                form_errors.extend(address_form.errors.values())
                form_errors.extend(avatar_phone_form.errors.values())

                # Collect non-field errors
                form_errors.extend(form.non_field_errors())
                form_errors.extend(address_form.non_field_errors())
                form_errors.extend(avatar_phone_form.non_field_errors())

                # Collect errors from formsets
                def collect_formset_errors(formset, name):
                    for error in formset.non_form_errors():
                        form_errors.append(f"{name} Error: {error}")
                    for i, errors in enumerate(formset.errors, 1):
                        if errors:
                            form_errors.append(f"{name} {i} Error: {errors}")

                collect_formset_errors(skill_formset, "Skill")
                collect_formset_errors(education_formset, "Education")
                collect_formset_errors(experience_formset, "Experience")
                collect_formset_errors(certification_formset, "Certification")
                collect_formset_errors(project_formset, "Project")
                collect_formset_errors(sociallink_formset, "Social Link")

                messages.warning(request, 'Please correct the errors in your form.')
        else:
            # Initialize forms and formsets for GET request
            form = UpdateResumeForm(instance=resume)
            address_form = AddressForm(instance=address)
            avatar_phone_form = UpdateAvatarPhoneForm(instance=user)
            skill_formset = ResumeSkillFormSet(prefix='skills', instance=resume)
            education_formset = ResumeEducationFormSet(prefix='education', instance=resume)
            experience_formset = ResumeExperienceFormSet(prefix='experience', instance=resume)
            certification_formset = ResumeCertificationFormSet(prefix='certification', instance=resume)
            project_formset = ResumeProjectFormSet(prefix='project', instance=resume)
            sociallink_formset = ResumeSocialLinkFormSet(prefix='social_link', instance=resume)

        context = {
            'form': form,
            'address_form': address_form,
            'avatar_phone_form': avatar_phone_form,
            'skill_formset': skill_formset,
            'education_formset': education_formset,
            'experience_formset': experience_formset,
            'certification_formset': certification_formset,
            'project_formset': project_formset,
            'sociallink_formset': sociallink_formset,
            'form_errors': form_errors,
        }
        return render(request, 'applicant/create-resume.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')

    
# view resume details
def resume_info(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    resume = Resume.objects.get(pk=pk)

    context = {'resume': resume}
    return render(request, 'applicant-profile.html', context)

def view_resume(request):
    try:
        resume = Resume.objects.get(user=request.user)  # Get the current user's resume
        resume_file = resume.upload_resume
    except Resume.DoesNotExist:
        resume_file = None

    return render(request, 'applicant/view_resume.html', {'resume_file': resume_file})
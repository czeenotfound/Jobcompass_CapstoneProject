from django.shortcuts import render, redirect
from django.forms import inlineformset_factory, BaseInlineFormSet
from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Resume,Skill, Education, Experience, Certification,Project, SocialLink
from django.forms import formset_factory
from .forms import UpdateResumeForm, SkillForm, EducationForm, ExperienceForm, CertificationForm, ProjectForm, SocialLinkForm
from address.forms import AddressForm
from users.models import User
from users.forms import UpdateAvatarPhoneForm
from django.http import JsonResponse


class SkillFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass

class EducationFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass
    
class ExperienceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass
        
class CertificationFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass

class ProjectFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass

class SocialLinkFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass


"""
Resume Creation System Overview:

This module handles the comprehensive resume creation process including:
1. Personal Information
2. Contact Details
3. Skills
4. Education History
5. Work Experience
6. Certifications
7. Projects
8. Social Links

Key Features:
- Multiple form handling with formsets
- File upload support
- Address management
- Profile picture handling
- Comprehensive validation
- Error handling for all components
"""

def create_resume(request):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Verify user is an applicant
    if request.user.is_applicant:
        # Get or create resume instance for the user
        resume, created = Resume.objects.get_or_create(user=request.user)
        address = resume.address if resume.address else None
        user = request.user

        # Initialize formsets for all resume components
        # Each formset allows multiple entries with deletion capability
        
        # Skills formset - for technical and soft skills
        ResumeSkillFormSet = inlineformset_factory(
            Resume,
            Skill, 
            form=SkillForm, 
            formset=SkillFormSet, 
            extra=1, 
            can_delete=True
        )
        
        # Education formset - for academic history
        ResumeEducationFormSet = inlineformset_factory(
            Resume, 
            Education, 
            form=EducationForm, 
            formset=EducationFormSet, 
            extra=1, 
            can_delete=True
        )
        
        # Experience formset - for work history
        ResumeExperienceFormSet = inlineformset_factory(
            Resume, Experience, 
            form=ExperienceForm, 
            formset=ExperienceFormSet, 
            extra=1, 
            can_delete=True
        )
        
        # Certification formset - for professional certifications
        ResumeCertificationFormSet = inlineformset_factory(
            Resume, Certification, 
            form=CertificationForm, 
            formset=CertificationFormSet, 
            extra=1, 
            can_delete=True
        )
        
        # Project formset - for portfolio projects
        ResumeProjectFormSet = inlineformset_factory(
            Resume, Project, 
            form=ProjectForm, 
            formset=ProjectFormSet, 
            extra=1, 
            can_delete=True
        )
        
        # Social Links formset - for professional profiles
        ResumeSocialLinkFormSet = inlineformset_factory(
            Resume, SocialLink, 
            form=SocialLinkForm, 
            formset=SocialLinkFormSet, 
            extra=1, 
            can_delete=True
        )

        form_errors = []  # Initialize error collection list

        if request.method == 'POST':
            # Handle form submission
            # Initialize all forms with POST data
            form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
            address_form = AddressForm(request.POST, instance=address)
            avatar_phone_form = UpdateAvatarPhoneForm(request.POST, request.FILES, instance=user)
            
            # Initialize all formsets with POST data
            skill_formset = ResumeSkillFormSet(request.POST, prefix='skills', instance=resume)
            education_formset = ResumeEducationFormSet(request.POST, prefix='education', instance=resume)
            experience_formset = ResumeExperienceFormSet(request.POST, prefix='experience', instance=resume)
            certification_formset = ResumeCertificationFormSet(request.POST, prefix='certification', instance=resume)
            project_formset = ResumeProjectFormSet(request.POST, prefix='project', instance=resume)
            sociallink_formset = ResumeSocialLinkFormSet(request.POST, prefix='social_link', instance=resume)

            # Validate all forms and formsets
            if form.is_valid() and address_form.is_valid() and avatar_phone_form.is_valid() and skill_formset.is_valid() and education_formset.is_valid() and experience_formset.is_valid() and certification_formset.is_valid() and project_formset.is_valid() and sociallink_formset.is_valid():
                # Save resume but don't commit yet
                resume_instance = form.save(commit=False)
                user.has_resume = True

                # Update user's basic information
                user.first_name = avatar_phone_form.cleaned_data['first_name']
                user.last_name = avatar_phone_form.cleaned_data['last_name']
                user.save() 

                # Save address information
                address_instance = address_form.save(commit=False)
                address_instance.user = user
                address_instance.save()
                
                # Link address to resume and save
                resume_instance.address = address_instance
                resume_instance.save()
                
                # Save all other components
                avatar_phone_form.save()
                skill_formset.save()
                education_formset.save()
                experience_formset.save()
                certification_formset.save()
                project_formset.save()
                sociallink_formset.save()

                messages.info(request, 'Your resume is now active. You can start applying for jobs.')
                return redirect('applicant-profile', pk=user.pk)
            else:
                # Comprehensive error collection from all forms
                
                # Collect main form errors
                form_errors.extend(form.errors.values())
                form_errors.extend(address_form.errors.values())
                form_errors.extend(avatar_phone_form.errors.values())

                # Collect non-field errors
                form_errors.extend(form.non_field_errors())
                form_errors.extend(address_form.non_field_errors())
                form_errors.extend(avatar_phone_form.non_field_errors())

                # Helper function to collect formset errors
                def collect_formset_errors(formset, name):
                    for error in formset.non_form_errors():
                        form_errors.append(f"{name} Error: {error}")
                    for i, errors in enumerate(formset.errors, 1):
                        if errors:
                            form_errors.append(f"{name} {i} Error: {errors}")

                # Collect errors from all formsets
                collect_formset_errors(skill_formset, "Skill")
                collect_formset_errors(education_formset, "Education")
                collect_formset_errors(experience_formset, "Experience")
                collect_formset_errors(certification_formset, "Certification")
                collect_formset_errors(project_formset, "Project")
                collect_formset_errors(sociallink_formset, "Social Link")

                messages.warning(request, 'Please correct the errors in your form.')
        else:
            # Handle GET request
            # Initialize empty forms and formsets
            form = UpdateResumeForm(instance=resume)
            address_form = AddressForm(instance=address)
            avatar_phone_form = UpdateAvatarPhoneForm(instance=user)
            
            # Initialize empty formsets
            skill_formset = ResumeSkillFormSet(prefix='skills', instance=resume)
            education_formset = ResumeEducationFormSet(prefix='education', instance=resume)
            experience_formset = ResumeExperienceFormSet(prefix='experience', instance=resume)
            certification_formset = ResumeCertificationFormSet(prefix='certification', instance=resume)
            project_formset = ResumeProjectFormSet(prefix='project', instance=resume)
            sociallink_formset = ResumeSocialLinkFormSet(prefix='social_link', instance=resume)

        # Prepare context with all forms and errors
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
        # Handle unauthorized access
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
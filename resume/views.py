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
            extra=1, 
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

                address.country_name = request.POST.get('country_name', '')
                address.state_name = request.POST.get('state_name', '')
            

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
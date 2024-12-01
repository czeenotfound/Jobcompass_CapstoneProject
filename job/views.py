from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import messages
from .models import Job, SaveJob, Application, ApplicationStatus, JobFair, RequiredSkill, Job_Responsibilities, Job_Experience, JobFairRegistration
from address.forms import AddressForm
from address.models import Address
from django.db.models.functions import Coalesce
from users.models import User
from company.models import Company
from .forms import CreateJobForm, UpdateJobForm, ApplicationStatusForm, CreateJobFairForm, UpdateJobFairForm
from django.db.models import Count, Q, Exists, OuterRef, Subquery,  Value
from job.filter import JobFairfilter


@login_required(login_url='login')
def job_info(request, pk):
    job = get_object_or_404(
        Job.objects.annotate(
            has_applied=Exists(
                Application.objects.filter(
                    user=request.user,
                    job=OuterRef('pk')
                )
            ),
            is_saved=Exists(
                SaveJob.objects.filter(
                    user=request.user,
                    job=OuterRef('pk')
                )
            )
        ),
        pk=pk
    )
    # Check if the user is authenticated
    if request.user.is_authenticated:
        if request.user.is_applicant:  # Assuming you have a boolean field 'is_applicant' in the custom User model
            has_applied = Application.objects.filter(user=request.user, job=pk).exists()
            is_saved = SaveJob.objects.filter(user=request.user, job=job).exists()
        else:
            has_applied = False
            is_saved = False
    else:
        has_applied = False  # Not logged in, so cannot apply
        is_saved = False  # Not logged in, so cannot save
    

    context = {'job': job, 'has_applied': has_applied, 'is_saved': is_saved}
    return render(request, 'job/job-info.html', context)


def job_fair_info(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login/Register required to proceed.')
        return redirect('login')
     

    jobfair = get_object_or_404(JobFair.objects.annotate(
        is_registered=Exists(
            JobFairRegistration.objects.filter(
                user=request.user,
                jobfair=OuterRef('pk')
            )
        )
    ), pk=pk)

    context = {
        'jobfair': jobfair,
    }

    return render(request, 'job/job-fair-info.html', context)


@login_required(login_url='login')
def job_application(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get all applications of the logged-in user
    applications = Application.objects.filter(
        user=request.user
    ).select_related('job', 'job__company', 'applicationstatus')

    # Total number of applications
    total_jobs = applications.count()

    # Count of applications by status
    status_counts = Application.objects.filter(user=request.user).values(
        'applicationstatus__status'
    ).annotate(count=Count('applicationstatus__status'))

    context = {
        'applications': applications,
        'total_jobs': total_jobs,
        'status_counts': {item['applicationstatus__status']: item['count'] for item in status_counts},
    }
    return render(request, 'applicant/job-application.html', context)


@login_required(login_url='login')
def view_job_application(request, pk):
    # Fetch the application by its primary key
    application = get_object_or_404(Application, pk=pk)
    job = get_object_or_404(
        Job.objects.annotate(
            has_applied=Exists(
                Application.objects.filter(
                    user=request.user,
                    job=OuterRef('pk')
                )
            ),
            is_saved=Exists(
                SaveJob.objects.filter(
                    user=request.user,
                    job=OuterRef('pk')
                )
            )
        ),
        pk=pk
    )
    # Optional: Ensure only authorized users (employer or applicant) can access it
    if request.user != application.job.company.user and request.user != application.user:
        return redirect('dashboard')  # Redirect unauthorized users

    # Pass the application details to the template
    context = {
        'application': application,
        'job': job
    }
    return render(request, 'applicant/view-job-application.html', context)


@login_required(login_url='login')
def job_savedjobs(request):
    # Get all applications of the logged-in user
    save_job = SaveJob.objects.filter(
        user=request.user
    ).select_related('job', 'job__company')

    # Total number of applications
    total_jobs = save_job.count()

    context = {
        'save_job': save_job,
        'total_jobs': total_jobs,
    }
    return render(request, 'applicant/job-savedjobs.html', context)


@login_required(login_url='login')
def application_analytics(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch all applications for the logged-in user
    applications = Application.objects.filter(user=request.user).select_related('job', 'job__company', 'applicationstatus', 'job__industry')
    # Total number of applications
    total_jobs = applications.count()

    # Get the count of applications by status
    status_counts = applications.values('applicationstatus__status').annotate(count=Count('applicationstatus')).order_by('-count')
    status_labels = [item['applicationstatus__status'] for item in status_counts]
    status_values = [item['count'] for item in status_counts]

    accepted_count = next((item['count'] for item in status_counts if item['applicationstatus__status'] == 'ACCEPTED'), 0)
    rejected_count = next((item['count'] for item in status_counts if item['applicationstatus__status'] == 'REJECTED'), 0)

     # Count of applications per industry
    industry_counts = applications.values(
        'job__industry__name'
    ).annotate(count=Count('job__industry__name')).order_by('-count')

    # Collect industry names and counts
    industry_names = [item['job__industry__name'] for item in industry_counts]
    industry_values = [item['count'] for item in industry_counts]

    # Salary data for jobs
    salary_data = applications.values(
        'job__salary_min', 'job__salary_max'
    )

    # Calculate average salary for each application
    salary_averages = [
        (item['job__salary_min'] + item['job__salary_max']) / 2 if item['job__salary_min'] and item['job__salary_max'] else 0
        for item in salary_data
    ]

    # Pass the data to the template
    context = {
        'applications': applications,
        'total_jobs': total_jobs,
        'status_labels': status_labels,  # For chart labels
        'status_values': status_values,  # For chart data

        'accepted_count': accepted_count,
        'rejected_count': rejected_count,

        'industry_names': industry_names,
        'industry_values': industry_values,
        'salary_averages': salary_averages,
    }

    return render(request, 'applicant/application-analytics.html', context)




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

class RequiredSkillFormSet(BaseInlineFormSet):
    def clean(self):
        # Ensure at least one skill is added
        super().clean()
        skills = [form.cleaned_data.get('skill_name') for form in self.forms if form.cleaned_data.get('skill_name')]
        
        if not skills:
            raise ValidationError("Please add at least one required skill.")

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

class JobResponsibilitiesFormSet(BaseInlineFormSet):
    def clean(self):
        # Ensure at least one responsibility is added
        super().clean()
        responsibilities = [form.cleaned_data.get('res_name') for form in self.forms if form.cleaned_data.get('res_name')]
        
        if not responsibilities:
            raise ValidationError("Please add at least one job responsibility.")
        
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

class JobExperienceFormSet(BaseInlineFormSet):
    def clean(self):
        # Ensure at least one experience entry is added
        super().clean()

        # Check for at least one valid Job Experience entry
        experiences = [form.cleaned_data for form in self.forms if form.cleaned_data.get('exp_name')]

        if not experiences:
            raise ValidationError("Please add at least one job experience.")

        # Validate that all required fields are filled
        for form in self.forms:
            if form.cleaned_data:  # Ensure form is not empty
                if not form.cleaned_data.get('exp_name') or not form.cleaned_data.get('exp_years') or not form.cleaned_data.get('exp_description'):
                    raise ValidationError("Please fill in all fields for each job experience entry.")

        return self.cleaned_data

@login_required(login_url='login')
def create_job(request): 
    if request.user.is_employer and request.user.has_company:
        try:
            company = Company.objects.get(user=request.user)

            # Check company verification status
            if company.verification_status == "Pending":
                messages.warning(request, "Your company verification is pending. You cannot post a job until it is verified.")
                return redirect('dashboard')  
            elif company.verification_status == "Rejected":
                messages.error(request, "Your company verification was rejected. Please contact support for assistance.")
                return redirect('dashboard')  
        except Company.DoesNotExist:
            messages.error(request, "You do not have a company profile. Please create one first.")
            return redirect('register-company')

        # Create formsets with custom base formset for validation
        SkillFormSet = inlineformset_factory(
            Job, 
            RequiredSkill, 
            form=RequiredSkillForm, 
            formset=RequiredSkillFormSet,
            extra=3,  
            can_delete=True
        )
        
        ResponsibilityFormSet = inlineformset_factory(
            Job, 
            Job_Responsibilities, 
            form=JobResponsibilitiesForm, 
            formset=JobResponsibilitiesFormSet,
            extra=3,  
            can_delete=True
        )

        ExperienceFormSet = inlineformset_factory(
            Job, 
            Job_Experience, 
            form=JobExperienceForm, 
            formset=JobExperienceFormSet,
            extra=2,  
            can_delete=True
        )

        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            skill_formset = SkillFormSet(request.POST, prefix='skills')
            responsibility_formset = ResponsibilityFormSet(request.POST, prefix='responsibilities')
            experience_formset = ExperienceFormSet(request.POST, prefix='experiences')    
    
            form_errors = []

            if form.is_valid():
                if skill_formset.is_valid() and responsibility_formset.is_valid() and experience_formset.is_valid():
                    var = form.save(commit=False)
                    var.user = request.user
                    var.company = request.user.company
                    company_industry = request.user.company.industry
                    
                    if company_industry:
                        var.industry = company_industry
                    else:
                        messages.warning(request, 'Your company does not have an associated industry.')
                        return redirect('create-job')

                    # Create or update the Address
                    location, created = Address.objects.get_or_create(
                        region=request.POST.get('region'),
                        province=request.POST.get('province'),
                        city=request.POST.get('city'),
                        barangay=request.POST.get('barangay'),
                        street=request.POST.get('street', '')
                    )
                    
                    var.location = location
                    var.save()

                    # Save formsets
                    skill_formset.instance = var
                    responsibility_formset.instance = var
                    experience_formset.instance = var
                    
                    skill_formset.save()
                    responsibility_formset.save()
                    experience_formset.save()

                    messages.info(request, 'New Job has been created')
                    return redirect('dashboard')
                else:
                    # Collect formset errors
                    if not skill_formset.is_valid():
                        for error in skill_formset.non_form_errors():
                            form_errors.append(f"Skills Error: {error}")
                        for i, form_errors_list in enumerate(skill_formset.errors, 1):
                            if form_errors_list:
                                form_errors.append(f"Skill {i} Error: {form_errors_list}")
                    
                    if not responsibility_formset.is_valid():
                        for error in responsibility_formset.non_form_errors():
                            form_errors.append(f"Responsibilities Error: {error}")
                        for i, form_errors_list in enumerate(responsibility_formset.errors, 1):
                            if form_errors_list:
                                form_errors.append(f"Responsibility {i} Error: {form_errors_list}")
                    
                    if not experience_formset.is_valid():
                        for error in experience_formset.non_form_errors():
                            form_errors.append(f"Experiences Error: {error}")
                        for i, form_errors_list in enumerate(experience_formset.errors, 1):
                            if form_errors_list:
                                form_errors.append(f"Experience {i} Error: {form_errors_list}")

            context = {
                'form': form,
                'skill_formset': skill_formset,
                'responsibility_formset': responsibility_formset,
                'experience_formset': experience_formset,
                'form_errors': form_errors
            }
            return render(request, 'job/create-job.html', context)
        
        else:
            # GET request
            form = CreateJobForm()
            skill_formset = SkillFormSet(prefix='skills')
            responsibility_formset = ResponsibilityFormSet(prefix='responsibilities')
            experience_formset = ExperienceFormSet(prefix='experiences')
            
            context = {
                'form': form,
                'skill_formset': skill_formset,
                'responsibility_formset': responsibility_formset,
                'experience_formset': experience_formset,
            }
            return render(request, 'job/create-job.html', context)
    else:
        messages.info(request, 'Permission Denied!')
        return redirect('dashboard')

@login_required(login_url='login')
def update_job(request, pk):
    job = Job.objects.get(pk=pk)
    address = job.location if job.location else Address()

    # Formsets for skills, responsibilities, and experiences
    SkillFormSet = inlineformset_factory(
        Job, 
        RequiredSkill, 
        form=RequiredSkillForm, 
        formset=RequiredSkillFormSet,
        extra=3,  # Adjust extra forms if needed
        can_delete=True
    )

    ResponsibilityFormSet = inlineformset_factory(
        Job, 
        Job_Responsibilities, 
        form=JobResponsibilitiesForm, 
        formset=JobResponsibilitiesFormSet,
        extra=3,  # Adjust extra forms if needed
        can_delete=True
    )

    ExperienceFormSet = inlineformset_factory(
        Job, 
        Job_Experience, 
        form=JobExperienceForm, 
        formset=JobExperienceFormSet,
        extra=1,  # Adjust extra forms if needed
        can_delete=True
    )

    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        address_form = AddressForm(request.POST, instance=address)
        skill_formset = SkillFormSet(request.POST, prefix='skills', instance=job)
        responsibility_formset = ResponsibilityFormSet(request.POST, prefix='responsibilities', instance=job)
        experience_formset = ExperienceFormSet(request.POST, prefix='experiences', instance=job)

        if form.is_valid() and address_form.is_valid() and skill_formset.is_valid() and responsibility_formset.is_valid() and experience_formset.is_valid():
            # Save address and job
            address_instance = address_form.save()
            job = form.save(commit=False)
            job.location = address_instance
            job.save()

            # Save formsets (skills, responsibilities, experiences)
            skill_formset.save()
            responsibility_formset.save()
            experience_formset.save()

            messages.info(request, 'Job information has been updated')
            return redirect('manage-jobs')
        else:
            messages.warning(request, 'There were errors in the form submission')
            return redirect('update-job', pk=pk)
    else:
        # GET request
        form = UpdateJobForm(instance=job)
        address_form = AddressForm(instance=address)
        skill_formset = SkillFormSet(prefix='skills', instance=job)
        responsibility_formset = ResponsibilityFormSet(prefix='responsibilities', instance=job)
        experience_formset = ExperienceFormSet(prefix='experiences', instance=job)

    context = {
        'form': form,
        'address_form': address_form,
        'skill_formset': skill_formset,
        'responsibility_formset': responsibility_formset,
        'experience_formset': experience_formset,
    }
    return render(request, 'job/update-job.html', context)
    


@login_required(login_url='login')
def activate_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    job.is_available = True
    job.save()

    messages.success(request, f"Job '{job.title}' has been activated.")

    return redirect('manage-jobs')  

@login_required(login_url='login')
def deactivate_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    job.is_available = False
    job.save()

    messages.success(request, f"Job '{job.title}' has been deactivated.")

    return redirect('manage-jobs') 
    
def apply(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login/Register required to proceed.')
        return redirect('login')
     
    if request.user.is_authenticated and request.user.is_applicant:
        if not request.user.has_resume:
            messages.warning(request, 'You need to register/upload a resume before applying to jobs.')
            return redirect('dashboard')

        job = Job.objects.get(pk=pk)
        if Application.objects.filter(user=request.user, job=pk).exists():
            
            messages.warning(request, 'Permission Denied')
            return redirect('dashboard')
        else:
            application = Application.objects.create(
                job=job,
                user=request.user,
            )

            # Create the associated ApplicationStatus
            ApplicationStatus.objects.create(
                application=application,
                status='SUBMITTED'
            )

            messages.info(request, 'You have successfully applied! Please see dashboard')
            return redirect('dashboard')
    else:
        messages.info(request, 'Please login to continue')
        return redirect('login')

@login_required(login_url='login')
def unapply(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login/Register required to proceed.')
        return redirect('login')

    if request.user.is_authenticated and request.user.is_applicant:
        job = get_object_or_404(Job, pk=pk)
        application = Application.objects.filter(user=request.user, job=job).first()

        if application:
            # Check the application status
            application_status = ApplicationStatus.objects.filter(application=application).first()

            if application_status and application_status.status == 'ACCEPTED':
                messages.warning(request, 'You cannot withdraw your application because it has already been accepted.')
            else:
                # Delete the application if not accepted
                application.delete()
                messages.success(request, 'You have successfully withdrawn your application.')
        else:
            messages.warning(request, 'You have not applied to this job or the application has already been withdrawn.')

        return redirect('dashboard')
    
    else:
        messages.info(request, 'You must be an applicant to withdraw your application.')
        return redirect('dashboard')
    
def save_job(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login/Register required to proceed.')
        return redirect('login')
     
    if request.user.is_applicant:
        if not request.user.has_resume:
            messages.warning(request, 'You need to register/upload a resume before applying to jobs.')
            return redirect('dashboard')

        job = get_object_or_404(Job, pk=pk)

        # Check if the job is already saved by the user
        saved_job = SaveJob.objects.filter(user=request.user, job=job).first()

        if saved_job:
            # If the job is already saved, delete it (unsave)
            saved_job.delete()
            messages.success(request, 'You have successfully unsaved the job. Please see your dashboard.')
        else:
            # If the job is not saved, save it
            SaveJob.objects.create(job=job, user=request.user)
            messages.success(request, 'You have successfully saved the job!')

        return redirect('dashboard')
    
    else:
        messages.info(request, 'This feature is only available for applicants.')
        return redirect('dashboard')

    
def unsave_job(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login/Register required to proceed.')
        return redirect('login')
     
    if request.user.is_applicant:
        job = get_object_or_404(Job, pk=pk)

        # Check if the job is already saved by the user
        saved_job = SaveJob.objects.filter(user=request.user, job=job).first()
        
        if saved_job:
            saved_job.delete()
            messages.success(request, 'You have successfully unsaved the job.')
        else:
            messages.warning(request, 'This job was not saved by you.')

        return redirect('dashboard')
    else:
        messages.info(request, 'This feature is only available for applicants.')
        return redirect('dashboard')
    
# ?????????????????????  JOB FAIR  ?????????????????????????????
# JOB FAIR


@login_required(login_url='login')
def job_fair(request):
    jobfairs = JobFair.objects.filter(is_active=True)\
        .annotate(
            is_registered=Exists(
                JobFairRegistration.objects.filter(
                    user=request.user,
                    jobfair=OuterRef('pk')
                )
            )
        ).order_by('-posted_date')

    context = {
        'jobfairs': jobfairs,
    }

    return render(request, 'job/applicant-jobfairs.html', context)


@login_required(login_url='login')
def all_job_fair(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login/Register required to proceed.')
        return redirect('login')
    
    jobfair_filter = JobFairfilter(request.GET, queryset=JobFair.objects.filter(is_active=True) \
         .annotate(
            is_registered=Exists(
                JobFairRegistration.objects.filter(
                    user=request.user,
                    jobfair=OuterRef('pk')
                )
            )
        ).order_by('-posted_date') \
        .select_related('company', 'industry', 'location') \
        .order_by('-posted_date'))
    
    context = {'jobfair_filter':  jobfair_filter}
    
    return render(request, 'job/applicant-alljobfairs.html', context)

def job_fair_register(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login/Register required to proceed.')
        return redirect('login')
     
    job_fair = get_object_or_404(JobFair, pk=pk)

    if JobFairRegistration.objects.filter(user=request.user, jobfair=job_fair).exists():
        return redirect('jobfair_success', pk=pk)  # Redirect to a success page if already registered

    registration = JobFairRegistration(user=request.user, jobfair=job_fair)
    registration.save()

    return redirect('jobfair_success', pk=pk)

@login_required(login_url='login')
def jobfair_success(request, pk):
    job_fair = get_object_or_404(JobFair, pk=pk)
    return render(request, 'job/jobfair_success.html', {'job_fair': job_fair})

@login_required(login_url='login')
def jobfair_registration(request):
    registrations = JobFairRegistration.objects.filter(user=request.user)

    total_registration = registrations.count()
    
    context = {
        'registrations': registrations,
        'total_jobs': total_registration,
    }
    return render(request, 'applicant/applicant-jobfair-registration.html', context)


@login_required(login_url='login')
def create_job_fair(request): 
    if request.user.is_employer and request.user.has_company:
        try:
            company = Company.objects.get(user=request.user)

            # Check company verification status
            if company.verification_status == "Pending":
                messages.warning(request, "Your company verification is pending. You cannot post a job until it is verified.")
                return redirect('dashboard')  
            elif company.verification_status == "Rejected":
                messages.error(request, "Your company verification was rejected. Please contact support for assistance.")
                return redirect('dashboard')  
        except Company.DoesNotExist:
            messages.error(request, "You do not have a company profile. Please create one first.")
            return redirect('register-company')

        if request.method == 'POST':
            form = CreateJobFairForm(request.POST, request.FILES)
            if form.is_valid():
                var = form.save(commit=False)
                var.user = request.user
                var.company = request.user.company

                # Create or update the Address
                location, created = Address.objects.get_or_create(
                    region=request.POST.get('region'),
                    province=request.POST.get('province'),
                    city=request.POST.get('city'),
                    barangay=request.POST.get('barangay'),
                    street=request.POST.get('street', '')
                )
                
                var.location = location

                var.save()
                messages.info(request, 'New Job Fair has been created')
                return redirect('manage-job-fairs')
            else:
                messages.warning(request, 'Something went wrong')
                return redirect('create-job-fair')
        else:
            form = CreateJobFairForm
            context = {'form': form,}
            return render(request, 'job/create-job-fair.html', context) 
    else:
        messages.info(request,'Permission Denied!')
        return redirect('dashboard')

@login_required(login_url='login')
def update_job_fair(request, pk):
    if request.user.is_employer and request.user.has_company:
        try:
            company = Company.objects.get(user=request.user)

            # Check company verification status
            if company.verification_status == "Pending":
                messages.warning(request, "Your company verification is pending. You cannot post a job until it is verified.")
                return redirect('dashboard')  
            elif company.verification_status == "Rejected":
                messages.error(request, "Your company verification was rejected. Please contact support for assistance.")
                return redirect('dashboard')  
        except Company.DoesNotExist:
            messages.error(request, "You do not have a company profile. Please create one first.")
            return redirect('register-company')
        
        jobfair = JobFair.objects.get(pk=pk)
        address = jobfair.location if jobfair.location else Address()

        if request.method == 'POST':
            form = UpdateJobFairForm(request.POST, request.FILES, instance=jobfair)
            address_form = AddressForm(request.POST, instance=address)

            if form.is_valid() and address_form.is_valid():
                address_instance = address_form.save()

                jobfair = form.save(commit=False)
                jobfair.location = address_instance 
                jobfair.save()

                messages.info(request, 'Job Fair information has been updated')
                return redirect('manage-job-fairs')
            else:
                messages.error(request, 'There was an error in updating job fair.')
                return redirect('manage-job-fairs')
        else:
            form = UpdateJobFairForm(instance=jobfair)
            address_form = AddressForm(instance=address)

        context = {
            'form': form,
            'address_form': address_form,
        }
        return render(request, 'job/update-jobfair.html', context)
    else:
        messages.info(request,'Permission Denied!')
        return redirect('dashboard')

def activate_job_fair(request, pk):
    if request.user.is_employer and request.user.has_company:
        jobfair = get_object_or_404(JobFair, pk=pk)
        
        jobfair.is_active = True
        jobfair.save()

        messages.success(request, f"Job Fair '{jobfair.title}' has been activated.")

        return redirect('manage-job-fairs')  
    else:
        messages.info(request,'Permission Denied!')
        return redirect('dashboard')

def deactivate_job_fair(request, pk):
    if request.user.is_employer and request.user.has_company:
        jobfair = get_object_or_404(JobFair, pk=pk)
        
        jobfair.is_active = False
        jobfair.save()

        messages.success(request, f"Job Fair '{jobfair.title}' has been deactivated.")

        return redirect('manage-job-fairs') 
    else:
        messages.info(request,'Permission Denied!')
        return redirect('dashboard')
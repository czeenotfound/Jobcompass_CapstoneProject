from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import messages
from .models import Job, SaveJob, Application, ApplicationStatus, JobFair, RequiredSkill, Job_Responsibilities, Job_IdealCandidates, Job_Benefits, Job_Experience, Job_Education, JobFairRegistration, Interview, Offer, Feedback
from address.forms import AddressForm
from address.models import Address, COUNTRY_CHOICES
from django.db.models.functions import Coalesce
from users.models import User
from company.models import Company
from .forms import CreateJobForm, UpdateJobForm, CreateJobFairForm, UpdateJobFairForm, RequiredSkillForm, JobResponsibilitiesForm, JobIdealCandidatesForm, JobBenefitsForm, JobExperienceForm, JobEducationForm
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
            ),
             application_status=Coalesce(
                Subquery(
                    ApplicationStatus.objects.filter(
                        application__job=OuterRef('pk'),
                        application__user=request.user
                    ).values('status')[:1]  
                ),
                Value('NOT_APPLIED') 
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
    application = get_object_or_404(Application, pk=pk)
   
    if request.user != application.job.company.user and request.user != application.user:
        return redirect('dashboard') 

    interviews = application.interview_set.all().order_by('interview_date')
    offer = application.offer_set.all().order_by('offer_date')
    feedback = application.feedback_set.all().order_by('feedback_date')

    context = {
        'application': application,
        'interviews': interviews,  
        'offers': offer,
        'feedbacks': feedback,
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
    status_labels = [item['applicationstatus__status'] for item in status_counts if item['applicationstatus__status']]
    status_values = [item['count'] for item in status_counts if item['applicationstatus__status']]

    # Count specific status values
    accepted_count = next((item['count'] for item in status_counts if item['applicationstatus__status'] == 'ACCEPTED'), 0)
    rejected_count = next((item['count'] for item in status_counts if item['applicationstatus__status'] == 'REJECTED'), 0)
    interview_count = next((item['count'] for item in status_counts if item['applicationstatus__status'] == 'INTERVIEW'), 0)
    offered_count = next((item['count'] for item in status_counts if item['applicationstatus__status'] == 'OFFERED'), 0)
    
    # Calculate response rate (applications that moved beyond SUBMITTED)
    total_responded = sum(item['count'] for item in status_counts 
                          if item['applicationstatus__status'] and item['applicationstatus__status'] != 'SUBMITTED')
    response_rate = (total_responded / total_jobs * 100) if total_jobs > 0 else 0
    
    # Calculate interview success rate
    interview_success_rate = ((interview_count + offered_count + accepted_count) / total_jobs * 100) if total_jobs > 0 else 0
    
    # Calculate offer success rate
    offer_success_rate = ((offered_count + accepted_count) / total_jobs * 100) if total_jobs > 0 else 0

    # Count of applications per industry
    industry_counts = applications.values(
        'job__industry__name'
    ).annotate(count=Count('job__industry__name')).order_by('-count')

    # Collect industry names and counts
    industry_names = [item['job__industry__name'] for item in industry_counts if item['job__industry__name']]
    industry_values = [item['count'] for item in industry_counts if item['job__industry__name']]

    # Salary data for jobs
    salary_data = applications.values(
        'job__salary_min', 'job__salary_max'
    )

    # Calculate average salary for each application
    salary_averages = [
        (item['job__salary_min'] + item['job__salary_max']) / 2 if item['job__salary_min'] and item['job__salary_max'] else 0
        for item in salary_data
    ]
    
    # Get applications over time (by month)
    from django.db.models.functions import TruncMonth
    apps_by_month = applications.annotate(
        month=TruncMonth('submit_date')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Format for chart
    months = [item['month'].strftime('%b %Y') if item['month'] else 'Unknown' for item in apps_by_month]
    monthly_counts = [item['count'] for item in apps_by_month]
    
    # Job type breakdown
    job_type_counts = applications.values('job__employment_job_type').annotate(
        count=Count('job__employment_job_type')
    ).order_by('-count')
    
    job_types = [item['job__employment_job_type'] for item in job_type_counts if item['job__employment_job_type']]
    job_type_values = [item['count'] for item in job_type_counts if item['job__employment_job_type']]
    
    # Response time analysis - get average days to first status change
    from django.db.models import F
    from django.db.models.functions import ExtractDay
    
    # Get applications with status changes
    applications_with_status = applications.filter(applicationstatus__isnull=False)
    
    # Pass the data to the template
    context = {
        'applications': applications,
        'total_jobs': total_jobs,
        'status_labels': status_labels,
        'status_values': status_values,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'interview_count': interview_count,
        'offered_count': offered_count,
        'response_rate': round(response_rate, 1),
        'interview_success_rate': round(interview_success_rate, 1),
        'offer_success_rate': round(offer_success_rate, 1),
        'industry_names': industry_names,
        'industry_values': industry_values,
        'salary_averages': salary_averages,
        'months': months,
        'monthly_counts': monthly_counts,
        'job_types': job_types,
        'job_type_values': job_type_values,
    }

    return render(request, 'applicant/application-analytics.html', context)

class RequiredSkillFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass

class JobResponsibilitiesFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass

class Job_iDealCandidatesFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass

class jobBenefitsFormSet(BaseInlineFormSet):    
    def clean(self):
        super().clean()
        pass

class JobExperienceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass

class JobEducationFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        pass
 
 
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
            extra=1,  
            can_delete=True
        )
         
        ResponsibilityFormSet = inlineformset_factory(
            Job, 
            Job_Responsibilities, 
            form=JobResponsibilitiesForm, 
            formset=JobResponsibilitiesFormSet,
            extra=1,  
            can_delete=True
        )

        IdealCandidateFormSet = inlineformset_factory(
            Job, 
            Job_IdealCandidates, 
            form=JobIdealCandidatesForm, 
            formset=Job_iDealCandidatesFormSet,
            extra=1,  
            can_delete=True
        )

        BenefitsFormSet = inlineformset_factory(
            Job, 
            Job_Benefits, 
            form=JobBenefitsForm, 
            formset=jobBenefitsFormSet,
            extra=1,  
            can_delete=True
        )

        ExperienceFormSet = inlineformset_factory(
            Job, 
            Job_Experience, 
            form=JobExperienceForm, 
            formset=JobExperienceFormSet,
            extra=1,  
            can_delete=True
        )

        EducationFormSet = inlineformset_factory(
            Job, 
            Job_Education, 
            form=JobEducationForm, 
            formset=JobEducationFormSet,
            extra=1,  
            can_delete=True
        )

        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            skill_formset = SkillFormSet(request.POST, prefix='skills')
            responsibility_formset = ResponsibilityFormSet(request.POST, prefix='responsibilities')
            idealcandidate_formset = IdealCandidateFormSet(request.POST, prefix='idealcandidates')
            benefits_formset = BenefitsFormSet(request.POST, prefix='benefits')
            experience_formset = ExperienceFormSet(request.POST, prefix='experiences') 
            education_formset = EducationFormSet(request.POST, prefix='education')
    
            form_errors = []

            if form.is_valid():
                if skill_formset.is_valid() and responsibility_formset.is_valid() and idealcandidate_formset.is_valid() and benefits_formset.is_valid() and experience_formset.is_valid() and education_formset.is_valid():
                    var = form.save(commit=False)
                    var.user = request.user
                    var.company = request.user.company
                    company_industry = request.user.company.industry
                    
                    if company_industry:
                        var.industry = company_industry
                    else:
                        messages.warning(request, 'Your company does not have an associated industry.')
                        return redirect('create-job')

                    # Check if the employer wants to use the company location
                    use_company_location = request.POST.get('use_company_location') == 'true'

                    if use_company_location:
                        # Use the company's address as the job location
                        company_location = request.user.company.address
                        if company_location:
                            var.location = company_location
                        else:
                            messages.warning(request, 'Your company does not have a valid address.')
                            return redirect('create-job')
                    else:
                        # Create or update a custom Address
                        location, created = Address.objects.get_or_create(
                            country=request.POST.get('country'),
                            countrypostal=request.POST.get('countrypostal'),
                            region=request.POST.get('region'),
                            city=request.POST.get('city'),
                            street=request.POST.get('street', '')
                        )
                        var.location = location
                    var.save()

                    # Save formsets
                    skill_formset.instance = var
                    responsibility_formset.instance = var
                    idealcandidate_formset.instance = var
                    benefits_formset.instance = var
                    experience_formset.instance = var
                    education_formset.instance = var
                    
                    skill_formset.save()
                    responsibility_formset.save()
                    idealcandidate_formset.save()
                    benefits_formset.save()
                    experience_formset.save()
                    education_formset.save()

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
                    
                    if not idealcandidate_formset.is_valid():
                        for error in idealcandidate_formset.non_form_errors():
                            form_errors.append(f"Ideal Candidates Error: {error}")
                        for i, form_errors_list in enumerate(idealcandidate_formset.errors, 1):
                            if form_errors_list:
                                form_errors.append(f"Ideal Candidate {i} Error: {form_errors_list}")

                    if not benefits_formset.is_valid():
                        for error in benefits_formset.non_form_errors():
                            form_errors.append(f"Benefits Error: {error}")
                        for i, form_errors_list in enumerate(benefits_formset.errors, 1):
                            if form_errors_list:
                                form_errors.append(f"Benefit {i} Error: {form_errors_list}")
                    
                    if not experience_formset.is_valid():
                        for error in experience_formset.non_form_errors():
                            form_errors.append(f"Experiences Error: {error}")
                        for i, form_errors_list in enumerate(experience_formset.errors, 1):
                            if form_errors_list:
                                form_errors.append(f"Experience {i} Error: {form_errors_list}")

                    if not education_formset.is_valid():
                        for error in education_formset.non_form_errors():
                            form_errors.append(f"Educations Error: {error}")
                        for i, form_errors_list in enumerate(education_formset.errors, 1):
                            if form_errors_list:
                                form_errors.append(f"Education {i} Error: {form_errors_list}")

            context = {
                'form': form,
                'skill_formset': skill_formset,
                'responsibility_formset': responsibility_formset,
                'idealcandidate_formset': idealcandidate_formset,
                'benefits_formset': benefits_formset,
                'experience_formset': experience_formset,
                'education_formset' : education_formset,
                'country_choices': COUNTRY_CHOICES, 
                'form_errors': form_errors
            }
            return render(request, 'job/create-job.html', context)
        
        else:
            # GET request
            form = CreateJobForm()
            skill_formset = SkillFormSet(prefix='skills')
            responsibility_formset = ResponsibilityFormSet(prefix='responsibilities')
            idealcandidate_formset = IdealCandidateFormSet(prefix='idealcandidates')
            benefits_formset = BenefitsFormSet(prefix='benefits')
            experience_formset = ExperienceFormSet(prefix='experiences')
            education_formset = EducationFormSet(prefix="education")
            
            context = {
                'form': form,
                'skill_formset': skill_formset,
                'responsibility_formset': responsibility_formset,
                'idealcandidate_formset': idealcandidate_formset,
                'benefits_formset': benefits_formset,
                'experience_formset': experience_formset,
                'education_formset' : education_formset,
                'country_choices': COUNTRY_CHOICES, 
            }
            return render(request, 'job/create-job.html', context)
    else:
        messages.info(request, 'Permission Denied!')
        return redirect('dashboard')
    
@login_required(login_url='login')
def delete_job(request, pk):
    if request.user.is_employer and request.user.has_company:
        job = get_object_or_404(Job, pk=pk)
        
        # Ensure the user owns this job
        if job.user != request.user:
            messages.error(request, "You don't have permission to delete this job.")
            return redirect('manage-jobs')
        
        job_title = job.title
        job.delete()
        messages.success(request, f"Job '{job_title}' has been deleted successfully.")
        return redirect('manage-jobs')
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
        extra=1,  # Adjust extra forms if needed
        can_delete=True
    )

    ResponsibilityFormSet = inlineformset_factory(
        Job, 
        Job_Responsibilities, 
        form=JobResponsibilitiesForm, 
        formset=JobResponsibilitiesFormSet,
        extra=1,  # Adjust extra forms if needed
        can_delete=True
    )

    IdealcandidateFormset = inlineformset_factory(
        Job,
        Job_IdealCandidates,
        form=JobIdealCandidatesForm,
        formset=Job_iDealCandidatesFormSet,
        extra=1,
        can_delete=True
    )

    BenefitsFormset = inlineformset_factory(
        Job,
        Job_Benefits,
        form=JobBenefitsForm,
        formset=jobBenefitsFormSet,
        extra=1,
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

    EducationFormSet = inlineformset_factory(
        Job, 
        Job_Education, 
        form=JobEducationForm, 
        formset=JobEducationFormSet,
        extra=1,  
        can_delete=True
    )


    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        address_form = AddressForm(request.POST, instance=address)
        skill_formset = SkillFormSet(request.POST, prefix='skills', instance=job)
        responsibility_formset = ResponsibilityFormSet(request.POST, prefix='responsibilities', instance=job)
        idealcandidate_formset = IdealcandidateFormset(request.POST, prefix='idealcandidates', instance=job)
        benefits_formset = BenefitsFormset(request.POST, prefix='benefits', instance=job)
        experience_formset = ExperienceFormSet(request.POST, prefix='experiences', instance=job)
        education_formset = EducationFormSet(request.POST, prefix='education', instance=job)

        form_errors = []

        if form.is_valid() and address_form.is_valid() and skill_formset.is_valid() and responsibility_formset.is_valid() and idealcandidate_formset.is_valid() and benefits_formset.is_valid() and experience_formset.is_valid() and education_formset.is_valid():
            # Save address and job
            address_instance = address_form.save()
            job = form.save(commit=False)
            job.location = address_instance
            job.save()

            # Save formsets (skills, responsibilities, idealcandidates, benefits, experiences)
            skill_formset.save()
            responsibility_formset.save()
            idealcandidate_formset.save()
            benefits_formset.save()
            experience_formset.save()
            education_formset.save()

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
        idealcandidate_formset = IdealcandidateFormset(prefix='idealcandidates', instance=job)
        benefits_formset = BenefitsFormset(prefix='benefits', instance=job)
        experience_formset = ExperienceFormSet(prefix='experiences', instance=job)
        education_formset = EducationFormSet(prefix='education', instance=job)

    context = {
        'form': form,
        'address_form': address_form,
        'skill_formset': skill_formset,
        'responsibility_formset': responsibility_formset,
        'idealcandidate_formset': idealcandidate_formset,
        'benefits_formset': benefits_formset,
        'experience_formset': experience_formset,
        'education_formset' : education_formset,
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
                company_industry = request.user.company.industry
                    
                if company_industry:
                    var.industry = company_industry
                else:
                    messages.warning(request, 'Your company does not have an associated industry.')
                    return redirect('create-job-fair')
                
                # Determine if the selected job fair type is "Virtual"
                job_fair_type = form.cleaned_data.get('fair_event_held')
                if job_fair_type == "Virtual":
                    # Use the company's address
                    var.location = company.address
                else:
                    # Create or update the Address based on form input
                    location, created = Address.objects.get_or_create(
                        country=request.POST.get('country'),
                        countrypostal=request.POST.get('countrypostal'),
                        region=request.POST.get('region'),
                        city=request.POST.get('city'),
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
            
            context = {
                'form': form,
                'country_choices': COUNTRY_CHOICES, 
            }
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
    
def delete_job_fair(request, pk):
    if request.user.is_employer and request.user.has_company:
        jobfair = get_object_or_404(JobFair, pk=pk)
        
        # Ensure the user owns this job
        if jobfair.user != request.user:
            messages.error(request, "You don't have permission to delete this job.")
            return redirect('manage-jobs')
        
        jobfair_title = jobfair.title
        jobfair.delete()
        messages.success(request, f"Job Fair '{jobfair_title}' has been deleted successfully.")
        return redirect('manage-job-fairs')
    else:
        messages.info(request, 'Permission Denied!')
        return redirect('dashboard')
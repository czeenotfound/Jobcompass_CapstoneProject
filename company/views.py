from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils.dateformat import format

from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Avg, F

from .models import Company, Employer
from address.models import Address
from job.models import Job, Application, ApplicationStatus, JobFair, Conversation, Message, JobFairRegistration, Interview, Offer, Feedback, Notification
from users.models import User
from resume.models import Resume

from .forms import UpdateCompanyForm, UpdateEmployerForm
from address.forms import AddressForm   
from job.forms import ApplicationForm, ApplicationStatusForm, InterviewForm, OfferForm, FeedbackForm
from users.forms import UpdateAvatarPhoneForm

# Create your views here.
# manage job postings

@login_required(login_url='login')
def manage_jobs(request):
    if request.user.is_employer:
        jobs = Job.objects.filter(user=request.user, company=request.user.company)
        
        context = {'jobs': jobs}
        return render(request, 'company/manage-jobs.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')

@login_required(login_url='login')
def manage_job_fair(request):
    if request.user.is_employer:
        jobfairs = JobFair.objects.filter(user=request.user, company=request.user.company)

        context = {
            'jobfairs': jobfairs
        }

        return render(request, 'company/manage-job-fairs.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
@login_required(login_url='login')
def job_analytics(request):
    if not request.user.is_employer:
        return redirect('login')
    
    jobs = Job.objects.filter(company__user=request.user).select_related('company', 'industry')
    total_jobs = jobs.count()
    
    # Get counts for all statuses across all jobs
    status_counts = ApplicationStatus.objects.filter(application__job__in=jobs).values('status').annotate(
        count=Count('id')
    )
    
    # Format status counts as a dictionary
    status_counts_dict = {status['status']: status['count'] for status in status_counts}

    # Ensure all statuses are included even if their count is 0
    all_statuses = ['SUBMITTED', 'UNDER_REVIEW', 'INTERVIEW', 'OFFERED', 'REJECTED', 'ACCEPTED']
    for status in all_statuses:
        if status not in status_counts_dict:
            status_counts_dict[status] = 0
    
    # Calculate total applications
    total_applications = sum(status_counts_dict.values())
    
    # Get per-job application stats
    job_stats = []
    for job in jobs:
        job_apps = job.application_set.all()
        job_app_count = job_apps.count()
        
        # Get status breakdown for this job
        job_status_counts = {}
        for status in all_statuses:
            job_status_counts[status] = job_apps.filter(applicationstatus__status=status).count()
        
        # Calculate conversion rates
        interview_rate = 0
        offer_rate = 0
        acceptance_rate = 0
        
        if job_status_counts['SUBMITTED'] + job_status_counts['UNDER_REVIEW'] > 0:
            interview_rate = (job_status_counts['INTERVIEW'] / 
                             (job_status_counts['SUBMITTED'] + job_status_counts['UNDER_REVIEW'] + 
                              job_status_counts['INTERVIEW'])) * 100
        
        if job_status_counts['INTERVIEW'] > 0:
            offer_rate = (job_status_counts['OFFERED'] / job_status_counts['INTERVIEW']) * 100
        
        if job_status_counts['OFFERED'] > 0:
            acceptance_rate = (job_status_counts['ACCEPTED'] / job_status_counts['OFFERED']) * 100
        
        job_stats.append({
            'job': job,
            'application_count': job_app_count,
            'status_counts': job_status_counts,
            'interview_rate': round(interview_rate, 1),
            'offer_rate': round(offer_rate, 1),
            'acceptance_rate': round(acceptance_rate, 1)
        })
    
    # Get applications over time (last 30 days)
    from django.utils import timezone
    from datetime import timedelta
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_applications = Application.objects.filter(
        job__in=jobs, 
        submit_date__gte=thirty_days_ago
    ).order_by('submit_date')
    
    # Group by date
    from django.db.models.functions import TruncDate
    applications_by_date = recent_applications.annotate(
        date=TruncDate('submit_date')
    ).values('date').annotate(count=Count('id')).order_by('date')
    
    # Format for chart
    dates = [item['date'].strftime('%Y-%m-%d') for item in applications_by_date]
    app_counts = [item['count'] for item in applications_by_date]
    
    registered_job_fairs = JobFairRegistration.objects.filter(jobfair__company__user=request.user).count()

    context = {
        'jobs': jobs,
        'job_stats': job_stats,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'status_counts': status_counts_dict,
        'registered_job_fairs': registered_job_fairs,
        'dates': dates,
        'app_counts': app_counts,
    }

    return render(request, 'company/job-analytics.html', context)
    
@login_required(login_url='login')
def job_applicants(request, pk):
    if request.user.is_employer:
        job = get_object_or_404(Job, pk=pk)
        applicants = job.application_set.all().order_by('-submit_date')
        interview_form = InterviewForm()
        offer_form = OfferForm()
        feedback_form = FeedbackForm()
        
        # Handle status updates
        if request.method == 'POST':
            
            application_id = request.POST.get('application_id')
            new_status = request.POST.get('status')
            
            if application_id and new_status:
                application = get_object_or_404(Application, pk=application_id)
                
                # Check if the employer is authorized to update this application
                if request.user == application.job.company.user:
                    # Get or create ApplicationStatus
                    application_status, created = ApplicationStatus.objects.get_or_create(application=application)
                    
                    application_status.status = new_status
                    application_status.save()

                    status_display = dict(ApplicationStatus.STATUS_CHOICES)[new_status]

                    # Start a conversation if it doesn't exist
                    conversation, convo_created = Conversation.objects.get_or_create(application=application)

                    # If a new conversation is created, send an initial message
                    if convo_created:
                        Message.objects.create(
                            conversation=conversation,
                            sender=request.user,
                            content=f"The status of your application for '{application.job.title}' has been updated to '{status_display}'."
                        )
                    else:
                        # Send a message notifying the status change
                        Message.objects.create(
                            conversation=conversation,
                            sender=request.user,
                            content=f"The status of your application for '{application.job.title}' has been updated to '{status_display}'."
                        )

                    if new_status == 'UNDER_REVIEW':
                        Notification.objects.create(
                            application=application,
                            message=f"Your application for '{application.job.title}' is now under review."
                        )

                    elif new_status == 'INTERVIEW':
                        interview_form = InterviewForm(request.POST)
                        if interview_form.is_valid():
                            interview = interview_form.save(commit=False)
                            interview.application = application
                            interview.save()

                            # Send notification for interview
                            Notification.objects.create(
                                application=application,
                                message=f"An interview has been scheduled for your application for '{application.job.title}'."
                            )

                    # Handle Offer creation
                    elif new_status == 'OFFERED':
                        offer_form = OfferForm(request.POST)
                        if offer_form.is_valid():
                            offer = offer_form.save(commit=False)
                            offer.application = application
                            offer.save()
                            
                            Notification.objects.create(
                                application=application,
                                message=f"A job offer has been made for your application for '{application.job.title}'."
                            )

                    # Handle Feedback creation
                    elif new_status in ['REJECTED', 'ACCEPTED']:
                        feedback_form = FeedbackForm(request.POST)
                        if feedback_form.is_valid():
                            feedback = feedback_form.save(commit=False)
                            feedback.application = application
                            feedback.feedback_type = 'APPLICANT' if new_status == 'REJECTED' else 'INTERVIEWER'
                            feedback.save()
                            
                            Notification.objects.create(
                                application=application,
                                message=f"Feedback has been provided for your application for '{application.job.title}'."
                            )

                    messages.success(request, f"Application status updated to {dict(ApplicationStatus.STATUS_CHOICES)[new_status]}")
                    return redirect('job-applicants', pk=pk)
                else:
                    messages.warning(request, "Unauthorized to update this application.")

        context = {
            'job': job,
            'interview_form': interview_form,
            'offer_form': offer_form,
            'feedback_form': feedback_form,
            'applicants': applicants
        }
        return render(request, 'company/job-applicants.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')

# job applicants 
@login_required(login_url='login')
def jobfair_registers(request, pk):
    if request.user.is_employer:
        jobfair = JobFair.objects.get(pk=pk)
        applicants = jobfair.jobfairregistration_set.all().order_by('-submit_date')
        context = {'jobfair':jobfair, 'applicants':applicants}
        return render(request, 'company/jobfair-registers.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
    
@login_required
def view_applicant_resume(request, applicant_id):
    if not request.user.is_employer:
        messages.warning(request, "Permission Denied.")
        return redirect('dashboard')
    
    applicant = get_object_or_404(User, id=applicant_id)
    
    # Update status to UNDER_REVIEW when viewing resume
    applications = Application.objects.filter(user=applicant)
    for application in applications:
        status, created = ApplicationStatus.objects.get_or_create(application=application)
        if status.status == 'SUBMITTED':
            status.status = 'UNDER_REVIEW'
            status.save()
            
            # Create notification
            Notification.objects.create(
                application=application,
                message="Your application is now under review."
            )

    try:
        resume = Resume.objects.get(user=applicant)
        resume_file = resume.upload_resume
    except Resume.DoesNotExist:
        resume_file = None

    return render(request, 'employer/view_resume.html', {'resume_file': resume_file, 'applicant': applicant})

@login_required(login_url='login')
def update_employer_profile(request):

    if request.user.is_employer:
        employer = Employer.objects.get(user=request.user)
        address = employer.address if employer.address else Address()
        user = request.user  # Get the logged-in user

        if request.method == 'POST':
            employer_form = UpdateEmployerForm(request.POST, instance=employer)
            address_form = AddressForm(request.POST, instance=address)
            avatar_phone_form = UpdateAvatarPhoneForm(request.POST, request.FILES, instance=user)

            if employer_form.is_valid() and address_form.is_valid() and avatar_phone_form.is_valid():
                # Save employer form
                employer = employer_form.save()

                # Save the address and associate it with the employer
                address = address_form.save()
                employer.address = address
                employer.save()

                # Save avatar and phone
                avatar_phone_form.save()

                messages.success(request, 'Profile updated successfully!')
                return redirect('employer-profile', pk=employer.id)  # Replace with your profile page URL
            else:
                messages.error(request, 'There was an error in updating your profile.')
        else:
            employer_form = UpdateEmployerForm(instance=employer)
            address_form = AddressForm(instance=address)
            avatar_phone_form = UpdateAvatarPhoneForm(instance=user)

        context = {
            'employer_form': employer_form,
            'address_form': address_form,
            'avatar_phone_form': avatar_phone_form,
        }
        return render(request, 'profile/update-employer-profile.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
    
# register company
@login_required(login_url='login')
def register_company(request):

    today = date.today().isoformat() 
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_employer:
        company = Company.objects.get(user=request.user)
        address = company.address

        # Initialize form_errors list
        form_errors = []

        if request.method == 'POST':
            form = UpdateCompanyForm(request.POST, request.FILES, instance=company)
            address_form = AddressForm(request.POST, instance=address)

            # Validate both forms
            if form.is_valid() and address_form.is_valid():
                # Save the company instance
                var = form.save(commit=False)
                var.save()

                # Save the address instance and link the user to the address
                address_instance = address_form.save(commit=False)
                address_instance.user = request.user
                address_instance.save()

                # Associate address with the company
                company.address = address_instance
                company.save()

                # Update the user's company status
                user = request.user
                user.has_company = True
                user.save()

                messages.info(request, 'Your company is now active. You can start creating job ads.')
                return redirect('company-profile', pk=user.pk)
            else:
                # Collect errors from both forms
                if not form.is_valid():
                    for field, errors in form.errors.items():
                        for error in errors:
                            form_errors.append(f"Company {field}: {error}")
                
                if not address_form.is_valid():
                    for field, errors in address_form.errors.items():
                        for error in errors:
                            form_errors.append(f"Address {field}: {error}")

        else:
            form = UpdateCompanyForm(instance=company)
            address_form = AddressForm(instance=address)
            context = {
                'form': form,
                'address_form': address_form,
                'form_errors': form_errors,  # Pass errors to the template
                'today': today
            }
            return render(request, 'company/update-company.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')


# APPLICATION 

def update_application_status(request, pk):
    if request.user.is_employer:
        application = get_object_or_404(Application, pk=pk)
        
        # Check if the user is authorized to update the application status
        if request.user != application.job.company.user:
            return redirect('dashboard')  # Unauthorized access prevention

        # Get or create ApplicationStatus for this application
        application_status, created = ApplicationStatus.objects.get_or_create(application=application)
        
        if request.method == 'POST':
            form = ApplicationStatusForm(request.POST, instance=application_status)
            if form.is_valid():
                form.save()  # Save the updated status
                
                # Start a conversation if it doesn't exist
                conversation, convo_created = Conversation.objects.get_or_create(application=application)
                
                # If a new conversation is created, send an initial message
                if convo_created:
                    Message.objects.create(
                        conversation=conversation,
                        sender=request.user,
                        content=f"The status of your application for '{application.job.title}' has been updated to '{application_status.status}'."
                    )

                # Redirect to the manage jobs page
                return redirect('manage-jobs')
        else:
            form = ApplicationStatusForm(instance=application_status)

        context = {
            'form': form,
            'application': application
        }
        return render(request, 'company/update_application_status.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
    
def view_bir(request):
    try:
        # Get the BIR file for the company associated with the user
        company = Company.objects.get(user=request.user)
        bir_file = company.bir_file  # Access the BIR file field
    except Company.DoesNotExist:
        bir_file = None  # No BIR file available

    return render(request, 'company/view_bir.html', {'bir_file': bir_file})

def view_dti(request):
    try:
        # Get the DTI file for the company associated with the user
        company = Company.objects.get(user=request.user)
        dti_file = company.dti_file  # Access the DTI file field
    except Company.DoesNotExist:
        dti_file = None  # No DTI file available

    return render(request, 'company/view_dti.html', {'dti_file': dti_file})


@login_required
def start_conversation(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    # Ensure only the employer can initiate the conversation
    if request.user != application.job.company.user:
        return redirect('home')  # Unauthorized access prevention

    # Create a conversation if it doesn't already exist
    conversation, created = Conversation.objects.get_or_create(application=application)
    if created:
        # Optionally send an initial message (e.g., job details/requirements)
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content="Hello! Here are the details and requirements for the position."
        )

    return redirect('view_conversation', conversation_id=conversation.id)

@login_required
def view_conversation(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    
    # Ensure only authorized users can access this conversation
    if request.user != conversation.application.job.company.user and request.user != conversation.application.user:
        return redirect('dashboard')

    # Fetch messages related to this conversation
    messages = conversation.messages.order_by('timestamp')  # Fetch in chronological order

    context = {
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'company/view_conversation.html', context)


@login_required
def send_message(request, pk):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, pk=pk)
        
        # Ensure the user is part of this conversation
        if request.user != conversation.application.job.company.user and request.user != conversation.application.user:
            messages.error(request, "You are not authorized to send messages in this conversation.")
            return redirect('dashboard')  # Unauthorized access prevention
        
        content = request.POST.get('content')
        if content:
            new_message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
            
            # Mark the new message as read if needed (optional)
            new_message.is_read = True
            new_message.save()

        return redirect('inbox')
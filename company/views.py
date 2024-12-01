from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Avg, F

from .models import Company, Employer
from address.models import Address
from job.models import Job, Application, ApplicationStatus, JobFair, Conversation, Message, JobFairRegistration
from users.models import User
from resume.models import Resume

from .forms import UpdateCompanyForm, UpdateEmployerForm
from address.forms import AddressForm   
from job.forms import ApplicationForm, ApplicationStatusForm
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
        context = {'jobfairs': jobfairs}

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
    
      # Get counts for all statuses
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


    registered_job_fairs = JobFairRegistration.objects.filter(jobfair__company__user=request.user).count()

    context = {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'status_counts': status_counts_dict,
        'registered_job_fairs': registered_job_fairs,
    }

    return render(request, 'company/job-analytics.html', context)

# job applicants 
@login_required(login_url='login')
def job_applicants(request, pk):
    if request.user.is_employer:
        job = Job.objects.get(pk=pk)
        applicants = job.application_set.all().order_by('-submit_date')
        context = {'job':job, 'applicants':applicants}
        return render(request, 'company/job-applicants.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
    

@login_required
def view_applicant_resume(request, applicant_id):
    if not request.user.is_employer:
        # If the user is not an employer, redirect or show an error
        messages.warning(request, "Permission Denied.")
        return redirect('dashboard')
    
    # Get the applicant by ID
    applicant = get_object_or_404(User, id=applicant_id)

    # Check if the applicant has a resume
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
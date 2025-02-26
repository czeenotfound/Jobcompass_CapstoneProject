from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q, Count, Case, When, IntegerField, F

from job.models import Job, SaveJob, Application, ApplicationStatus, Conversation, Message
from company.models import Company, Employer
from resume.models import Resume
from django.db.models import Exists, OuterRef, Max, Prefetch, Subquery, Value
from django.db.models.functions import Coalesce
from users.models import User
from job.filter import Jobfilter
from resume.filter import Resumefilter
from django.contrib.auth.decorators import login_required
from job.filter import get_salary_range_choices

from django.db.models.functions import Lower


# # Create your views here.
@login_required(login_url='login')
def dashboard(request):
    job_filter = Jobfilter(request.GET, queryset=Job.objects.filter(is_available=True) \
        .annotate(
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
        ) \
        .select_related('company', 'industry', 'location') \
        .order_by('-posted_date_time'))

    job_filtered_count = job_filter.qs.count()

    resume_filter = Resumefilter(request.GET, queryset=Resume.objects.filter(user__has_resume=True) \
        .select_related('user', 'address') \
        .prefetch_related(
            'skills',
            'education',
            'experiences',
            'certifications',
            'projects',
            'social_links'
        ).order_by('?')  # Randomize the queryset
    ) 
    
    try:
        employer = Employer.objects.get(user=request.user)
        # Check if critical fields are missing
        is_profile_complete = all([
            employer.first_name,
            employer.last_name,
            employer.address,
        ])
    except Employer.DoesNotExist:
        # Employer profile does not exist
        employer = None
        is_profile_complete = False
        # Get the count of filtered results

    resume_filtered_count = resume_filter.qs.count()

    
    # Fetch the user's resume
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        resume = None

    # Recommended jobs based on resume details
    
    if resume:
        applicant_skills = list(resume.skills.values_list(Lower('name'), flat=True))

        recommended_jobs = Job.objects.filter(
            Q(industry=resume.industry) |
            Q(requiredskill__skill_name__in=applicant_skills)
        ).distinct() 

        recommended_jobs = recommended_jobs.annotate(
            industry_match=Case(
                When(industry=resume.industry, then=1), 
                default=0,
                output_field=IntegerField()
            ),
            skill_match_count=Count(
                "requiredskill",
                filter=Q(requiredskill__skill_name__in=applicant_skills)
            ),
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
        ).annotate(
            total_score=F("industry_match") + F("skill_match_count"),
            best_match=Case(
                When(total_score__gte=3, then=Value(True)),
                default=Value(False),
                output_field=IntegerField()
            ),
            not_suitable=Case(
                When(total_score__lte=1, then=Value(True)),  
                default=Value(False),
                output_field=IntegerField()
            )
        ).order_by("-total_score")

    else:
        recommended_jobs = Job.objects.none()


    recommended_jobs_count = recommended_jobs.count()

    context = {
        'job_filter': job_filter,
        'job_filtered_count': job_filtered_count,
        'resume_filtered_count': resume_filtered_count,
        'resume_filter': resume_filter,
        'salary_range_choices': get_salary_range_choices(),
        'recommended_jobs': recommended_jobs,
        'recommended_jobs_count': recommended_jobs_count,
        'is_profile_complete': is_profile_complete
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login')
def applicant_profile(request, pk):
    if pk != request.user.id:
        return redirect('applicant-profile', pk=request.user.id)
    
    if not request.user.is_applicant:
        return redirect('dashboard')

    try:
        resume = Resume.objects.get(user=request.user)  # Get the current user's resume
        resume_file = resume.upload_resume
    except Resume.DoesNotExist:
        resume_file = None

    context = {
        'user': request.user,
        'resume_file': resume_file
    }
    return render(request, 'profile/applicant-profile.html', context)


@login_required(login_url='login')
def view_resume_profile(request, pk):
    # Fetch the resume object by its primary key (pk)
    resume = get_object_or_404(Resume, pk=pk)

    try:
        resume = Resume.objects.get(pk=pk) 
        resume_file = resume.upload_resume
    except Resume.DoesNotExist:
        resume_file = None
    
    context = {
        'resume': resume,
        'resume_file': resume_file
    }
    return render(request, 'applicant/view_resume_profile.html', context)

@login_required(login_url='login')
def company_profile(request, pk):
    if pk != request.user.id:
        return redirect('company-profile', pk=request.user.id)

    if not request.user.is_employer:
        return redirect('dashboard')

    context = {'user': request.user}
    return render(request, 'profile/company-profile.html', context)

@login_required(login_url='login')
def employer_profile(request, pk):
    try:
        employer = Employer.objects.get(user=request.user)
        # Check if critical fields are missing
        is_profile_complete = all([
            employer.first_name,
            employer.last_name,
            employer.address,  # Check if address exists
        ])
    except Employer.DoesNotExist:
        # Employer profile does not exist
        employer = None
        is_profile_complete = False

    context = {
        'employer': employer,
        'is_profile_complete': is_profile_complete
    }
    return render(request, 'profile/employer-profile.html', context)


@login_required(login_url='login')
def inbox(request):
    # Filter conversations based on user role
    if request.user.is_applicant:
        conversations = Conversation.objects.filter(application__user=request.user)
    elif request.user.is_employer:
        conversations = Conversation.objects.filter(application__job__company__user=request.user)
    else:
        conversations = Conversation.objects.none()  # Empty queryset for safety
    
    # Optimize queries with select_related and prefetch_related
    conversations = (
        conversations
        .select_related(
            'application',  # Optimize the FK to Application
            'application__user',  # Optimize the FK to User
            'application__job',  # Optimize the FK to Job
            'application__job__company'  # Optimize the FK to Company
        )
        .prefetch_related(
            Prefetch(
                'messages',
                queryset=Message.objects.order_by('timestamp'),
                to_attr='prefetched_messages'  # Prefetch and store messages as a list
            )
        )
        .annotate(latest_message_timestamp=Max('messages__timestamp'))  # Annotate for ordering
        .order_by('-latest_message_timestamp')
    )

    # Select the first conversation to display messages
    first_conversation = conversations.first()
    inboxs = getattr(first_conversation, 'prefetched_messages', []) if first_conversation else []

    # Mark all unread messages as read
    if first_conversation:
        Message.objects.filter(conversation=first_conversation, is_read=False).update(is_read=True)

    context = {
        'conversations': conversations,
        'inboxs': inboxs,
        'first_conversation': first_conversation,
    }
    return render(request, 'dashboard/inbox.html', context)



@login_required(login_url='login')
def user_settings(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps the user logged in after the password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('logout')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {
        'user': user,
        'form': form,
    }
    
    return render(request, 'dashboard/settings.html', context)
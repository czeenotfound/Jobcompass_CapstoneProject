from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from company.models import Company, Employer
from users.models import User
from resume.models import Resume
from industry.models import Industry
from users.forms import UserRegistrationForm
from job.models import Job, Application, JobFair, ApplicationStatus

def login_admin(request):
    logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        admin = authenticate(request, username=username, password=password)
        
        if admin is not None and admin.is_active and admin.is_superuser:
            login(request, admin)
            return redirect('admin-dashboard') 
        else:
            messages.warning(request, 'Invalid username or password, or you do not have permission to access this area.')
            return redirect('admin-login')
    
    return render(request, 'admin/admin-login.html')
    
def logout_admin(request):
    logout(request)
    messages.info(request, 'Your Session has ended.')
    return redirect('admin-login')

# # Create your views here.

@login_required(login_url='admin-login')
def admin_profile(request, pk):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
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
    return render(request, 'admin/admin-profile.html', context)

@login_required(login_url='admin-login')
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    # User Statistics
    total_users_active = User.objects.filter(is_active=True).count()
    total_users_inactive = User.objects.filter(is_active=False).count()
    
    # Applicant Statistics
    total_applicants = User.objects.filter(is_applicant=True).count()
    applicants_with_resume = User.objects.filter(is_applicant=True, has_resume=True).count()
    applicants_without_resume = total_applicants - applicants_with_resume
    
    # Employer Statistics
    total_employers = User.objects.filter(is_employer=True).count()
    verified_employers = User.objects.filter(is_employer=True, is_verified=True).count()
    pending_employers = total_employers - verified_employers
    
    # Company Statistics
    total_companies = Company.objects.count()
    verified_companies = Company.objects.filter(is_verified=True).count()
    pending_companies = Company.objects.filter(verification_status='Pending').count()
    
    # Job Statistics
    jobs_open = Job.objects.filter(is_available=True).count()
    jobs_closed = Job.objects.filter(is_available=False).count()
    
    # Application Statistics
    total_applications = Application.objects.count()
    pending_applications = ApplicationStatus.objects.filter(
        status__in=['SUBMITTED', 'UNDER_REVIEW']
    ).count()
    processed_applications = total_applications - pending_applications
    
    # Job Fair Statistics
    total_job_fairs = JobFair.objects.count()
    active_job_fairs = JobFair.objects.filter(is_active=True).count()
    upcoming_job_fairs = JobFair.objects.filter(
        start_date__gt=timezone.now().date()
    ).count()
    
    # Application Status Breakdown
    submitted_applications = ApplicationStatus.objects.filter(status='SUBMITTED').count()
    under_review_applications = ApplicationStatus.objects.filter(status='UNDER_REVIEW').count()
    interview_applications = ApplicationStatus.objects.filter(status='INTERVIEW').count()
    offered_applications = ApplicationStatus.objects.filter(status='OFFERED').count()
    accepted_applications = ApplicationStatus.objects.filter(status='ACCEPTED').count()
    rejected_applications = ApplicationStatus.objects.filter(status='REJECTED').count()

    jobs = Job.objects.all()
    resumes = Resume.objects.select_related('user').prefetch_related('skills').all()
    
    matching_stats = {
        'total_jobs': jobs.count(),
        'jobs_with_matches': 0,
        'total_matches': 0,
        'high_match_jobs': 0,
        'medium_match_jobs': 0,
        'low_match_jobs': 0,
    }

    for job in jobs:
        matching_resumes = resumes.filter(industry=job.industry).distinct()
        has_match = False
        
        if matching_resumes.exists():
            job_skills = list(job.requiredskill_set.values_list('skill_name', flat=True))
            if job_skills:
                for resume in matching_resumes:
                    applicant_skills = list(resume.skills.values_list('name', flat=True))
                    matched_skills = set(s.lower() for s in job_skills) & set(s.lower() for s in applicant_skills)
                    
                    if matched_skills:
                        match_percentage = (len(matched_skills) / len(job_skills)) * 100
                        if not has_match:
                            matching_stats['jobs_with_matches'] += 1
                            has_match = True
                            
                            if match_percentage >= 80:
                                matching_stats['high_match_jobs'] += 1
                            elif match_percentage >= 50:
                                matching_stats['medium_match_jobs'] += 1
                            else:
                                matching_stats['low_match_jobs'] += 1
                        
                        matching_stats['total_matches'] += 1

    # Calculate match percentage
    if matching_stats['total_jobs'] > 0:
        matching_stats['match_percentage'] = round(
            (matching_stats['jobs_with_matches'] / matching_stats['total_jobs']) * 100
        )
    else:
        matching_stats['match_percentage'] = 0

    context = {
        # User Statistics
        'total_users_active': total_users_active,
        'total_users_inactive': total_users_inactive,
        'total_applicants': total_applicants,
        'applicants_with_resume': applicants_with_resume,
        'applicants_without_resume': applicants_without_resume,
        'total_employers': total_employers,
        'verified_employers': verified_employers,
        'pending_employers': pending_employers,
        
        # Company Statistics
        'total_companies': total_companies,
        'verified_companies': verified_companies,
        'pending_companies': pending_companies,
        
        # Job Statistics
        'jobs_open': jobs_open,
        'jobs_closed': jobs_closed,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'processed_applications': processed_applications,
        
        # Job Fair Statistics
        'total_job_fairs': total_job_fairs,
        'active_job_fairs': active_job_fairs,
        'upcoming_job_fairs': upcoming_job_fairs,
        
        # Application Status Statistics
        'submitted_applications': submitted_applications,
        'under_review_applications': under_review_applications,
        'interview_applications': interview_applications,
        'offered_applications': offered_applications,
        'accepted_applications': accepted_applications,
        'rejected_applications': rejected_applications,

        'matching_stats': matching_stats,
    }
    
    return render(request, 'admin/admin-dashboard.html', context)

@login_required(login_url='admin-login')
def admin_manage_jobs(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    # Get filter parameters
    filter_type = request.GET.get('filter_type', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    job_status = request.GET.get('job_status', 'all')
    match_quality = request.GET.get('match_quality', 'all')
    min_match_percentage = request.GET.get('min_match_percentage')
    selected_industry = request.GET.get('industry', 'all')

    today = timezone.now()

    job_industry_ids = Job.objects.values_list('industry', flat=True).distinct()
    resume_industry_ids = Resume.objects.values_list('industry', flat=True).distinct()
    
    # Combine and get unique industry IDs
    all_industry_ids = set(job_industry_ids) | set(resume_industry_ids)
    
    # Get industry objects with names
    available_industries = Industry.objects.filter(id__in=all_industry_ids).order_by('name')
    
    
    # Base queryset

    all_jobs = Job.objects.all().select_related('company').order_by('-posted_date_time')
    alljobs = all_jobs

    jobs = Job.objects.all().order_by('-posted_date_time')
    
    # Apply date filters
    if filter_type == 'last_week':
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    elif filter_type == 'last_30_days':
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    elif filter_type == 'custom' and start_date:
        if not end_date:
            end_date = today.strftime('%Y-%m-%d')
    
    if start_date:
        jobs = jobs.filter(posted_date_time__date__gte=start_date)
    if end_date:
        jobs = jobs.filter(posted_date_time__date__lte=end_date)
    
    # Apply job status filter
    if job_status == 'open':
        jobs = jobs.filter(is_available=True)
    elif job_status == 'closed':
        jobs = jobs.filter(is_available=False)

    if selected_industry != 'all':
        jobs = jobs.filter(industry=selected_industry)

    all_jobs_stats = {
        'total': all_jobs.count(),
        'open': all_jobs.filter(is_available=True).count(),
        'closed': all_jobs.filter(is_available=False).count(),
    }

    # Get all resumes and their skills
    resumes = Resume.objects.select_related('user').prefetch_related('skills').all()

    matched_jobs_count = 0
    total_jobs = jobs.count()
    open_jobs_count = jobs.filter(is_available=True).count()
    closed_jobs_count = jobs.filter(is_available=False).count()

    jobs_with_matches = []
    
    # Initialize report data
    report_data = {
        'total_jobs': total_jobs,
        'open_jobs': open_jobs_count,
        'closed_jobs': closed_jobs_count,
        'jobs_with_matches': 0,
        'total_matches': 0,
        'match_percentage': 0,
        'high_match_jobs': 0,
        'medium_match_jobs': 0,
        'low_match_jobs': 0,
        'match_by_date': {},
    }

    # Process each job
    for job in jobs:
        job_date = job.posted_date_time.date().strftime('%Y-%m-%d')
        if job_date not in report_data['match_by_date']:
            report_data['match_by_date'][job_date] = {'total': 0, 'matches': 0}
        report_data['match_by_date'][job_date]['total'] += 1
        
        # Get matching resumes based on industry
        matching_resumes = resumes.filter(industry=job.industry).distinct()
        job_matches = []

        if matching_resumes.exists():
            job_skills = list(job.requiredskill_set.values_list('skill_name', flat=True))
            if job_skills:  # Only process if job has required skills
                job_skills_lower = [skill.lower() for skill in job_skills]

                for resume in matching_resumes:
                    applicant_skills = list(resume.skills.values_list('name', flat=True))
                    applicant_skills_lower = [skill.lower() for skill in applicant_skills]
                    exact_matches = []

                    # Find matching skills
                    for job_skill in job_skills:
                        job_skill_lower = job_skill.lower()
                        if job_skill_lower in applicant_skills_lower:
                            matching_skill = next(
                                (s for s in applicant_skills if s.lower() == job_skill_lower),
                                job_skill
                            )
                            exact_matches.append(matching_skill)

                    # Calculate match percentage and apply filters
                    if exact_matches:
                        match_percentage = round((len(exact_matches) / len(job_skills)) * 100)
                        
                        # Apply match quality filters
                        should_include = True
                        if min_match_percentage and match_percentage < float(min_match_percentage):
                            should_include = False
                        elif match_quality == 'high' and match_percentage < 80:
                            should_include = False
                        elif match_quality == 'medium' and (match_percentage < 50 or match_percentage >= 80):
                            should_include = False
                        elif match_quality == 'low' and match_percentage >= 50:
                            should_include = False

                        if should_include:
                            job_matches.append({
                                'user': resume.user,
                                'resume': resume,
                                'matched_skills': exact_matches,
                                'skill_match_count': len(exact_matches),
                                'skill_match_percentage': match_percentage
                            })

        # Add job to results if it has qualifying matches
        if job_matches:
            matched_jobs_count += 1
            report_data['jobs_with_matches'] += 1
            report_data['match_by_date'][job_date]['matches'] += 1
            
            # Update match quality statistics
            max_match_percentage = max(match['skill_match_percentage'] for match in job_matches)
            if max_match_percentage >= 80:
                report_data['high_match_jobs'] += 1
            elif max_match_percentage >= 50:
                report_data['medium_match_jobs'] += 1
            else:
                report_data['low_match_jobs'] += 1
            
            report_data['total_matches'] += len(job_matches)
            
            jobs_with_matches.append({
                'job': job,
                'matches': sorted(job_matches, key=lambda x: x['skill_match_percentage'], reverse=True),
                'match_count': len(job_matches)
            })

    # Calculate overall match percentage
    if total_jobs > 0:
        report_data['match_percentage'] = round((report_data['jobs_with_matches'] / total_jobs) * 100)
    
    # Sort match_by_date chronologically
    report_data['match_by_date'] = dict(sorted(report_data['match_by_date'].items()))

     # Enhanced report statistics
    enhanced_report = {
        'industry_breakdown': [],
        'recent_matches': {
            'last_7_days': 0,
            'last_30_days': 0,
            'trend_7_days': 'Stable',
            'trend_30_days': 'Stable'
        }
    }

    # Calculate industry breakdown
    for industry in available_industries:
        industry_jobs = jobs.filter(industry=industry)
        industry_matches = sum(1 for j in jobs_with_matches if j['job'].industry == industry)
        industry_resumes = resumes.filter(industry=industry).count()
        
        if industry_jobs.count() > 0:
            match_rate = round((industry_matches / industry_jobs.count()) * 100)
        else:
            match_rate = 0

        enhanced_report['industry_breakdown'].append({
            'name': industry.name,
            'total_jobs': industry_jobs.count(),
            'matched_jobs': industry_matches,
            'total_resumes': industry_resumes,
            'match_rate': match_rate
        })

    # Calculate time-based statistics
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)

    # Last 7 days matches
    recent_matches_7 = sum(
        data['matches'] 
        for date_str, data in report_data['match_by_date'].items() 
        if datetime.strptime(date_str, '%Y-%m-%d').date() >= last_week
    )

    # Last 30 days matches
    recent_matches_30 = sum(
        data['matches'] 
        for date_str, data in report_data['match_by_date'].items() 
        if datetime.strptime(date_str, '%Y-%m-%d').date() >= last_month
    )

    enhanced_report['recent_matches'].update({
        'last_7_days': recent_matches_7,
        'last_30_days': recent_matches_30
    })

    # Calculate averages and percentages
    if report_data['jobs_with_matches'] > 0:
        enhanced_report['avg_matches_per_job'] = round(report_data['total_matches'] / report_data['jobs_with_matches'], 1)
        enhanced_report['avg_match_percentage'] = round(sum(
            match['skill_match_percentage'] 
            for job in jobs_with_matches 
            for match in job['matches']
        ) / report_data['total_matches'], 1)
    else:
        enhanced_report['avg_matches_per_job'] = 0
        enhanced_report['avg_match_percentage'] = 0

    if total_jobs > 0:
        enhanced_report.update({
            'high_match_percentage': round((report_data['high_match_jobs'] / total_jobs) * 100),
            'medium_match_percentage': round((report_data['medium_match_jobs'] / total_jobs) * 100),
            'low_match_percentage': round((report_data['low_match_jobs'] / total_jobs) * 100)
        })
    else:
        enhanced_report.update({
            'high_match_percentage': 0,
            'medium_match_percentage': 0,
            'low_match_percentage': 0
        })

    context = {
        'jobs_with_matches': jobs_with_matches,
        'matched_jobs_count': matched_jobs_count,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
        'job_status': job_status,
        'match_quality': match_quality,
        'min_match_percentage': min_match_percentage,
        'total_jobs': len(jobs_with_matches),
        'open_jobs_count': sum(1 for j in jobs_with_matches if j['job'].is_available),
        'closed_jobs_count': sum(1 for j in jobs_with_matches if not j['job'].is_available),
        'report_data': report_data,
        'all_jobs': alljobs,  # Add all jobs to context
        'all_jobs_stats': all_jobs_stats,
        'available_industries': available_industries,
        'selected_industry': selected_industry,
        'enhanced_report': enhanced_report
    }

    return render(request, 'admin/admin-manage-jobs.html', context)
@login_required(login_url='admin-login')
def admin_manage_jobfairs(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    jobfairs = JobFair.objects.all()
    
    # Calculate statistics
    stats = {
        'total_jobfairs': jobfairs.count(),
        'active_jobfairs': jobfairs.filter(is_active=True).count(),
        'featured_jobfairs': jobfairs.filter(is_featured=True).count(),
        'companies_participating': JobFair.objects.values('company').distinct().count(),
    }
    
    # Get monthly statistics for the last 6 months
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_stats = (
        JobFair.objects
        .filter(posted_date__gte=six_months_ago)
        .annotate(month=TruncMonth('posted_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Format the monthly stats for the template
    formatted_monthly_stats = [
        {
            'month': item['month'].month,
            'year': item['month'].year,
            'count': item['count']
        }
        for item in monthly_stats
    ]

    # Get location statistics with proper address information
    location_stats = (
        JobFair.objects
        .select_related('location')  # Add this to efficiently fetch related Address
        .values('location__city', 'location__region')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    # Format location stats to combine city and region
    formatted_location_stats = [
        {
            'location': f"{item['location__city']}",
            'count': item['count']
        }
        for item in location_stats
    ]

    stats.update({
        'monthly_stats': formatted_monthly_stats,
        'location_stats': formatted_location_stats
    })
    
    context = {
        'jobfairs': jobfairs,
        'stats': stats,
    }
    
    return render(request, 'admin/admin-manage-jobfairs.html', context)

@login_required(login_url='admin-login')
def toggle_featured_status(request, pk):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    jobfair = get_object_or_404(JobFair, pk=pk)
    jobfair.is_featured = not jobfair.is_featured  # Toggle the is_featured status
    jobfair.save()

    messages.success(request, f"Job Fair '{jobfair.title}' featured status updated.")
    
    return redirect('admin-manage-jobfairs')

@login_required(login_url='admin-login')
def admin_employers(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin-login')
    
    # Get all users who are applicants
    employers = User.objects.filter(is_employer=True)

    context = {
        'employers': employers,
    }
    
    return render(request, 'admin/admin-employers.html', context)

@login_required(login_url='admin-login')
def admin_applicants(request):
    # Ensure the user is authenticated and authorized (optional, based on your requirements)
    if not request.user.is_authenticated or not request.user.is_staff:  # Example: Check if the user is an admin
        return redirect('admin-login')
    
    # Get all users who are applicants
    applicants = User.objects.filter(is_applicant=True)

    context = {
        'applicants': applicants,
    }

    return render(request, 'admin/admin-applicants.html', context)


@login_required(login_url='admin-login')
def admin_verification(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('admin-login')

    companies = Company.objects.all()

    # Calculate counts for each status
    pending_count = Company.objects.filter(verification_status='Pending').count()
    verified_count = Company.objects.filter(verification_status='Verified').count()
    rejected_count = Company.objects.filter(verification_status='Rejected').count()

    # Handle status update
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        new_status = request.POST.get('verification_status')
        company = get_object_or_404(Company, id=company_id)
        
        if new_status in ['Pending', 'Verified', 'Rejected']:
            company.verification_status = new_status
            company.is_verified = (new_status == 'Verified')
            company.save()
            messages.success(request, f"{company.company_name}'s status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status update.")
    
        return redirect('admin-verification')

    context = {
        'companies': companies,
        'pending_count': pending_count,
        'verified_count': verified_count,
        'rejected_count': rejected_count,
    }

    return render(request, 'admin/admin-verifications.html', context)



@login_required(login_url='login')  # Ensure only logged-in users can perform this action
def toggle_user_status(request, user_id):
    # Ensure the user has permissions (optional, e.g., admin-only toggle)
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('admin-dashboard')  # Adjust redirect as needed

    # Get the user object
    user = get_object_or_404(User, pk=user_id)

    # Toggle the user's active status
    user.is_active = not user.is_active
    user.save()

    # Provide feedback to the admin
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User {user.get_full_name()} has been {status}.")
    return redirect('admin-dashboard')  # Adjust redirect as needed


@login_required(login_url='login')
def admin_activate_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    job.is_available = True
    job.save()

    messages.success(request, f"Job '{job.title}' has been activated.")

    return redirect('admin-manage-jobs')  

@login_required(login_url='login')
def admin_deactivate_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    job.is_available = False
    job.save()

    messages.success(request, f"Job '{job.title}' has been deactivated.")

    return redirect('admin-manage-jobs') 

def admin_activate_job_fair(request, pk):
    if request.user.is_superuser:
        jobfair = get_object_or_404(JobFair, pk=pk)
        
        jobfair.is_active = True
        jobfair.save()

        messages.success(request, f"Job Fair '{jobfair.title}' has been activated.")

        return redirect('admin-manage-jobfairs')  
    else:
        messages.info(request,'Permission Denied!')
        return redirect('admin-dashboard')
    
    

def admin_deactivate_job_fair(request, pk):
    if request.user.is_superuser:
        jobfair = get_object_or_404(JobFair, pk=pk)
        
        jobfair.is_active = False
        jobfair.save()

        messages.success(request, f"Job Fair '{jobfair.title}' has been deactivated.")

        return redirect('admin-manage-jobfairs') 
    else:
        messages.info(request,'Permission Denied!')
        return redirect('admin-dashboard')
    

def admin_create_account(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.is_active = True  # Set user as inactive until email is verified
            user.save()

            role = form.cleaned_data.get('role')
            if role == 'applicant':
                user.is_applicant = True
                user.save()
                Resume.objects.get_or_create(
                    user=user,
                    defaults={
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                )
            elif role == 'employer':
                user.is_employer = True
                user.save()
                Company.objects.create(user=user)
                Employer.objects.get_or_create(
                    user=user,
                    defaults={
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                )

            messages.success(request, 'An account has been created.')
            return redirect('admin-create-account')
        else:
            # Handle form errors and display specific error messages
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

            # Stay on the current step if there are validation errors
            return render(request, 'admin/admin-create-account.html', {'form': form})
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'admin/admin-create-account.html',context)
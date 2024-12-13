from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from company.models import Company
from users.models import User
from resume.models import Resume
from job.models import Job, Application, JobFair

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
def dashboard(request):
    if not request.user.is_staff:
        return redirect('admin-login')

    
    return render(request, 'admin/admin.html')

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
    
    # Get counts
    total_applicants = User.objects.filter(is_applicant=True).count()
    total_companies = Company.objects.count()
    total_applications = Application.objects.count()
    total_users_active = User.objects.filter(is_active=True).count()
    total_users_inactive = User.objects.filter(is_active=False).count()
    jobs_open = Job.objects.filter(is_available=True).count()
    jobs_closed = Job.objects.filter(is_available=False).count()

    context = {
        'total_applicants': total_applicants,
        'total_companies': total_companies,
        'total_applications': total_applications,
        'total_users_active': total_users_active,
        'total_users_inactive': total_users_inactive,

        'jobs_open': jobs_open,
        'jobs_closed': jobs_closed,
    }
    
    return render(request, 'admin/admin-dashboard.html', context)

@login_required(login_url='admin-login')
def admin_manage_jobs(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    jobs = Job.objects.all()

    context={
        'jobs': jobs,
    }

    return render(request, 'admin/admin-manage-jobs.html', context)

@login_required(login_url='admin-login')
def admin_manage_jobfairs(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    jobfairs = JobFair.objects.all()

    context={
        'jobfairs': jobfairs,
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
        return redirect('dashboard')  # Adjust redirect as needed

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
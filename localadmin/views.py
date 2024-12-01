from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from company.models import Company
from users.models import User
from job.models import Application

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
def admin_profile(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-profile.html')

@login_required(login_url='admin-login')
def admin_settings(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-settings.html')

@login_required(login_url='admin-login')
def admin_acc_settings(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-acc-settings.html')

@login_required(login_url='admin-login')
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    # Get counts
    total_applicants = User.objects.filter(is_applicant=True).count()
    total_companies = Company.objects.count()
    total_applications = Application.objects.count()

    # Pass data to the template
    context = {
        'total_applicants': total_applicants,
        'total_companies': total_companies,
        'total_applications': total_applications,
    }
    
    return render(request, 'admin/admin-dashboard.html')

@login_required(login_url='admin-login')
def admin_manage_jobs(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-manage-jobs.html')

@login_required(login_url='admin-login')
def admin_manage_jobfairs(request):
    if not request.user.is_superuser:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-manage-jobfairs.html')

@login_required(login_url='admin-login')
def admin_employers(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-employers.html')

@login_required(login_url='admin-login')
def admin_applicants(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-applicants.html')


@login_required(login_url='admin-login')
def admin_reports(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    
    return render(request, 'admin/admin-report.html')

@login_required(login_url='admin-login')
def admin_verification(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('admin-login')

    companies = Company.objects.all()

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

    return render(request, 'admin/admin-verifications.html', {'companies': companies})
    

    return render(request, 'admin/admin-verifications.html')
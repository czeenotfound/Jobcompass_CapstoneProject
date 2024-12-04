from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from job.models import Job, JobFair
from job.filter import Jobfilter
from resume.models import Resume
from company.models import Company, Employer
from .forms import UserRegistrationForm
from job.filter import get_salary_range_choices
# Create your views here.

def home(request):
    logout(request)
    
    job_filter = Jobfilter(request.GET, queryset=Job.objects.filter(is_available=True) \
        .select_related('company', 'industry', 'location') \
        .order_by('-posted_date_time'))
    
    context = {
        'job_filter': job_filter,
        'salary_range_choices': get_salary_range_choices(),  # Pass to template
    }
    return render(request, 'index.html', context)

# ============ SIGN UP VIEWS ================= #


def register(request):
    logout(request)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email

            # Set the role based on the user's choice
            role = form.cleaned_data.get('role')
            if role == 'applicant':
                user.is_applicant = True
                user.save()
                Resume.objects.create(user=user)
            elif role == 'employer':
                user.is_employer = True
                user.save()
                Company.objects.create(user=user)
                Employer.objects.create(user=user)

            messages.success(request, 'Your account has been created successfully.')
            return redirect('login')
        else:
            # Handle form errors and display specific error messages
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/signup.html', context)
# ============ SIGN IN VIEWS ================= #

def login_user(request):
    logout(request)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        # Check if the user exists and is active
        if user is not None and user.is_active:
            if not user.is_active:
                messages.error(request, 'Your account has been deactivated. Please contact support for assistance.')
                return redirect('login')
            
            if user.is_applicant or user.is_employer:
                login(request, user)
                messages.success(request, 'Signed in successfully.')
                return redirect('dashboard') 
            else:
                messages.warning(request, 'Only applicants and employers can log in here.')
                return redirect('login')
        else:
            messages.warning(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    else:
        return render(request, 'users/login.html')
    
def logout_user(request):
    logout(request)
    messages.info(request, 'Your Session has ended.')
    return redirect('login')


def job_fair(request):
    jobfairs = JobFair.objects.filter(is_active=True)\
        .order_by('-posted_date')

    context = {
        'jobfairs': jobfairs,
    }
    return render(request, 'users/jobfair.html', context)
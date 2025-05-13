from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from job.models import Job, JobFair
from job.filter import Jobfilter
from resume.models import Resume
from company.models import Company, Employer
from .forms import UserRegistrationForm, OTPForm, PasswordResetRequestForm, SetNewPasswordForm

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

"""
User Authentication and Registration System Overview:

This module handles user authentication flows including:
1. User Registration (Applicant/Employer)
2. Email Verification
3. Login/Logout
4. Password Reset

Key Features:
- Multi-step registration process
- Role-based user creation (Applicant/Employer)
- Email verification with secure tokens
- Password reset functionality
- Session management
- Automatic profile creation based on role
"""

# Create your views here.

def home(request):
    logout(request)
    
    job_filter = Jobfilter(request.GET, queryset=Job.objects.filter(is_available=True) \
        .select_related('company', 'industry', 'location') \
        .order_by('-posted_date_time'))
    
    context = {
        'job_filter': job_filter
    }
    return render(request, 'index.html', context)

# ============ SIGN UP VIEWS ================= #

def register(request):
    # Ensure clean session start
    logout(request)  # Ensure user is logged out before registration

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        current_step = int(request.POST.get('current_step', 1))

        if form.is_valid():
            # Create user but don't save to DB yet
            user = form.save(commit=False)
            user.username = user.email  # Use email as username
            user.is_active = False      # User starts inactive until email verification

            # Set user role based on registration choice
            role = form.cleaned_data.get('role')
            if role == 'applicant':
                user.is_applicant = True
            elif role == 'employer':
                user.is_employer = True

            user.save()

            # Create associated profiles based on user role
            if user.is_applicant:
                # Create resume profile for applicant
                Resume.objects.get_or_create(
                    user=user,
                    defaults={
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                )
            elif user.is_employer:
                # Create company and employer profiles
                Company.objects.get_or_create(user=user)
                Employer.objects.get_or_create(
                    user=user,
                    defaults={
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                )

            # Generate secure verification token and URL
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )

            # Prepare and send verification email
            subject = "Verify Your Job Compass Account"
            context = {"user": user, "verification_link": verification_link}
            html_message = render_to_string("emails/verification_email.html", context)
            plain_message = render_to_string("emails/verification_email.txt", context)

            # Send both HTML and plain text versions
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email="Job Compass <no-reply@jobcompass.com>", 
                to=[user.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            messages.success(request, 'Your account has been created. Please check your email for the verification link.')
            return redirect('login')

        else:
            # Handle form validation errors
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

            messages.error(request, "There were errors in your submission. Please correct them and try again.")
            return render(request, 'users/signup.html', {'form': form, 'current_step': current_step})

    else:
        # Initial GET request - show empty form
        form = UserRegistrationForm()
        current_step = 1

    return render(request, 'users/signup.html', {'form': form, 'current_step': current_step})

def verify_email(request, uidb64, token):
    """
    Email verification view that validates the token and activates the user account.
    Uses Django's built-in token generator for security.
    """
    logout(request)

    try:
        # Decode the user ID and get user object
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Verify token and activate user
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('resend_verification_link')

def resend_verification_link(request):
    """
    Allows users to request a new verification link if the original expires.
    Includes security checks to prevent abuse.
    """
    logout(request)

    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        # Validate user exists and needs verification
        if not user:
            messages.error(request, "No account found with that email.")
            return redirect('resend_verification')

        if user.is_verified:
            messages.info(request, "Your account is already verified. You can log in.")
            return redirect('login')

        # Generate new verification token and URL
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = request.build_absolute_uri(
            reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        )

        # Send new verification email
        subject = "Verify Your Job Compass Account"
        context = {"user": user, "verification_link": verification_link}
        html_message = render_to_string("emails/verification_email.html", context)
        plain_message = render_to_string("emails/verification_email.txt", context)

        email_message = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email="Job Compass <no-reply@jobcompass.com>",
            to=[user.email],
        )
        email_message.attach_alternative(html_message, "text/html")
        email_message.send()

        messages.success(request, "A new verification link has been sent to your email.")
        return redirect('login')

    return render(request, 'users/resend_verification_link.html')

# ============ SIGN IN VIEWS ================= #

def login_user(request):
    """
    Handles user authentication with role-based redirections
    and account status validation.
    """
    logout(request)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.is_active:
            # Check account status
            if not user.is_active:
                messages.error(request, 'Your account has been deactivated. Please contact support for assistance.')
                return redirect('login')
            
            # Handle role-based login
            if user.is_applicant or user.is_employer:
                login(request, user)
                messages.success(request, 'Signed in successfully.')
                return redirect('dashboard') 
            else:
                return redirect('login')
        else:
            messages.warning(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    else:
        return render(request, 'users/login.html')
    
def logout_user(request):
    """
    Handles user logout and session cleanup.
    """
    logout(request)
    messages.info(request, 'Your Session has ended.')
    return redirect('login')

# ============ PASSWORD RESET VIEWS ================= #

def password_reset_request(request):
    """
    Handles password reset requests with secure token generation
    and email notification.
    """
    logout(request)

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            # Validate user exists
            if not user:
                messages.error(request, "No account found with that email.")
                return redirect('password_reset_request')

            # Generate secure reset token and URL
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
            )

            # Send password reset email
            subject = "Reset Your Password - Job Compass"
            context = {"user": user, "reset_link": reset_link}
            html_message = render_to_string("emails/password_reset_email.html", context)
            plain_message = render_to_string("emails/password_reset_email.txt", context)

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email="Job Compass <no-reply@jobcompass.com>",
                to=[user.email],
            )
            email_message.attach_alternative(html_message, "text/html")
            email_message.send()

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('login')

    else:
        form = PasswordResetRequestForm()

    return render(request, 'users/password_reset_request.html', {'form': form})

User = get_user_model()

def reset_password(request, uidb64, token):
    """
    Handles the actual password reset after token validation.
    Ensures secure password update process.
    """
    logout(request)

    try:
        # Decode user ID and validate token
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
        else:
            form = SetNewPasswordForm(user)
        return render(request, 'users/reset_password.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('password_reset_request')

# ============ DASHBOARD VIEWS ================= #

def job_fair(request):
    jobfairs = JobFair.objects.filter(is_active=True)\
        .order_by('-posted_date')

    context = {
        'jobfairs': jobfairs,
    }
    return render(request, 'users/jobfair.html', context)
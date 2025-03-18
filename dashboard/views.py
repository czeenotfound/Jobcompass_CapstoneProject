from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q, Count, Case, When, IntegerField, F, ExpressionWrapper
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import json
from django.views.decorators.http import require_POST

from job.models import Job, SaveJob, Application, ApplicationStatus, Conversation, Message, Job_Education, Job_Experience, Notification
from company.models import Company, Employer
from resume.models import Resume, Experience, Education
from django.db.models import Exists, OuterRef, Max, Prefetch, Subquery, Value
from django.db.models.functions import Coalesce
from users.models import User
from job.filter import Jobfilter
from resume.filter import Resumefilter
from django.contrib.auth.decorators import login_required
from rapidfuzz import fuzz, process
from django.db.models.functions import Lower


# # Create your views here.
@login_required(login_url='login')
def dashboard(request):
    try:
        employer = Employer.objects.get(user=request.user)
        company = Company.objects.get(user=request.user)
        company_jobs = Job.objects.filter(company=company, is_available=True)
        company_industries = company_jobs.values_list('industry', flat=True).distinct()
        
        base_queryset = Resume.objects.filter(user__has_resume=True) \
            .select_related('user', 'address') \
            .prefetch_related(
                'skills',
                'education',
                'experiences',
                'certifications',
                'projects',
                'social_links'
            )

        annotated_resumes = base_queryset.annotate(
            industry_match=Case(
                When(industry__in=company_industries, then=1),
                default=0,
                output_field=IntegerField()
            ),
            employment_match=Case(
                When(employment_job_type__in=company_jobs.values_list('employment_job_type', flat=True), then=1),
                default=0,
                output_field=IntegerField()
            ),
            location_match=Case(
                When(location_job_type__in=company_jobs.values_list('location_job_type', flat=True), then=1),
                default=0,
                output_field=IntegerField()
            ),
            total_match_score=F('industry_match') + F('employment_match') + F('location_match')
        ).order_by('-total_match_score', '?')

        if company.industry:
            annotated_resumes = annotated_resumes.filter(
                Q(industry=company.industry)
            ).distinct() 

        resume_filter = Resumefilter(request.GET, queryset=annotated_resumes)
        
        for resume in resume_filter.qs:
            applicant_skills = list(resume.skills.values_list('name', flat=True))
            applicant_skills_lower = [skill.lower() for skill in applicant_skills]
            
            matching_jobs = []
            for job in company_jobs:
                job_match_score = 0
                matches = []
                skill_matches = []
                
                if resume.industry == job.industry:
                    job_match_score += 1
                    matches.append('Industry')
                
                if resume.employment_job_type == job.employment_job_type:
                    job_match_score += 1
                    matches.append('Employment Type')
                
                if resume.location_job_type == job.location_job_type:
                    job_match_score += 1
                    matches.append('Location Type')
                
                if any(edu.education_level in Job_Education.objects.filter(job=job).values_list('education_level', flat=True) 
                      for edu in resume.education.all()):
                    job_match_score += 1
                    matches.append('Education')
                
                job_skills = list(job.requiredskill_set.values_list('skill_name', flat=True))
                job_skills_lower = [skill.lower() for skill in job_skills]
                
                exact_matches = []
                fuzzy_matches = []
                unmatched_skills = []
                
                for job_skill in job_skills:
                    job_skill_lower = job_skill.lower()
                    
                    if job_skill_lower in applicant_skills_lower:
                        original_skill = next((s for s in applicant_skills if s.lower() == job_skill_lower), job_skill)
                        exact_matches.append({
                            'job_skill': job_skill,
                            'resume_skill': original_skill,
                            'match_type': 'exact',
                            'similarity': 100
                        })
                        skill_matches.append(job_skill)
                        continue
                    
                    best_match = None
                    best_score = 0
                    
                    for app_skill in applicant_skills:
                        similarity = fuzz.partial_ratio(app_skill.lower(), job_skill_lower)
                        if similarity > 70 and similarity > best_score:
                            best_match = app_skill
                            best_score = similarity
                    
                    if best_match:
                        fuzzy_matches.append({
                            'job_skill': job_skill,
                            'resume_skill': best_match,
                            'match_type': 'fuzzy',
                            'similarity': best_score
                        })
                        skill_matches.append(job_skill)
                    else:
                        unmatched_skills.append(job_skill)
                
                skill_match_score = len(exact_matches) + (len(fuzzy_matches) * 0.5)
                
                if skill_match_score > 0:
                    job_match_score += min(skill_match_score, 2) 
                    matches.append('Skills')
                
                skill_match_details = {
                    'exact_matches': exact_matches,
                    'fuzzy_matches': fuzzy_matches,
                    'unmatched_skills': unmatched_skills,
                    'skill_match_score': skill_match_score,
                    'matched_skills': skill_matches
                }
                
                if job_match_score > 0:
                    matching_jobs.append({
                        'job': job,
                        'match_score': job_match_score,
                        'matching_criteria': matches,
                        'skill_match_details': skill_match_details
                    })
            
            matching_jobs.sort(key=lambda x: x['match_score'], reverse=True)
            resume.matching_jobs = matching_jobs
            
            max_score = 5
            
            best_job_score = matching_jobs[0]['match_score'] if matching_jobs else 0
            match_percentage = (best_job_score / max_score) * 100
            
            resume.best_match = match_percentage >= 70
            resume.good_match = 50 <= match_percentage < 70
            resume.not_suitable = match_percentage < 30

        resume_filtered_count = resume_filter.qs.count()
        is_profile_complete = all([
            employer.first_name,
            employer.last_name,
            employer.address,
        ])

    except (Employer.DoesNotExist, Company.DoesNotExist):
        employer = None
        company = None
        is_profile_complete = False
        resume_filter = None
        resume_filtered_count = 0
        company_jobs = []
    
    # Fetch the user's resume
    
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        resume = None

    if resume:
        base_queryset = Job.objects.filter(is_available=True)

        job_filter = Jobfilter(request.GET, queryset=base_queryset)
        filtered_jobs = job_filter.qs

        applicant_skills = list(resume.skills.values_list('name', flat=True))
        applicant_skills_lower = [skill.lower() for skill in applicant_skills]

        recommended_jobs = filtered_jobs.annotate(
            industry_match=Case(
                When(industry=resume.industry, then=1), 
                default=0, output_field=IntegerField()
            ),
            employment_match=Case(
                When(employment_job_type=resume.employment_job_type, then=1),
                default=0, output_field=IntegerField()
            ),
            location_match=Case(
                When(location_job_type=resume.location_job_type, then=1),
                default=0, output_field=IntegerField()
            ),
            has_applied=Exists(
                Application.objects.filter(user=request.user, job=OuterRef('pk'))
            ),
            is_saved=Exists(
                SaveJob.objects.filter(user=request.user, job=OuterRef('pk'))
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
        )

        recommended_jobs = recommended_jobs.filter(
            Q(industry=resume.industry)
        ).distinct() 

        job_list = list(recommended_jobs)
        final_jobs = []
        
        for job in job_list:
            job_skills = list(job.requiredskill_set.values_list('skill_name', flat=True))
            job_skills_lower = [skill.lower() for skill in job_skills]
            
            exact_matches = []
            fuzzy_matches = []
            unmatched_skills = []
            
            for job_skill in job_skills:
                job_skill_lower = job_skill.lower()
                
                if job_skill_lower in applicant_skills_lower:
                    original_skill = next((s for s in applicant_skills if s.lower() == job_skill_lower), job_skill)
                    exact_matches.append({
                        'job_skill': job_skill,
                        'resume_skill': original_skill,
                        'match_type': 'exact',
                        'similarity': 100
                    })
                    continue
                
                best_match = None
                best_score = 0
                
                for app_skill in applicant_skills:
                    similarity = fuzz.partial_ratio(app_skill.lower(), job_skill_lower)
                    if similarity > 70 and similarity > best_score: 
                        best_match = app_skill
                        best_score = similarity
                
                if best_match:
                    fuzzy_matches.append({
                        'job_skill': job_skill,
                        'resume_skill': best_match,
                        'match_type': 'fuzzy',
                        'similarity': best_score
                    })
                else:
                    unmatched_skills.append(job_skill)
            
            skill_match_count = len(exact_matches) + (len(fuzzy_matches) * 0.5)
            
            job.matched_skills = exact_matches + fuzzy_matches
            job.unmatched_skills = unmatched_skills
            job.skill_match_count = skill_match_count
            
            education_match = 0
            job_education_levels = list(Job_Education.objects.filter(job=job).values_list('education_level', flat=True))
            job_degrees = list(Job_Education.objects.filter(job=job).values_list('degree', flat=True))
            
            education_matches = []
            
            for user_edu in resume.education.all():
                if user_edu.education_level in job_education_levels:
                    level_match = True
                    level_match_data = {
                        'type': 'level',
                        'resume_value': user_edu.get_education_level_display(),
                        'job_value': dict(Education.EDUCATION_LEVEL_CHOICES).get(user_edu.education_level)
                    }
                    
                    degree_match = False
                    degree_match_data = None
                    
                    for job_degree in job_degrees:
                        if job_degree and user_edu.degree.strip().lower() == job_degree.strip().lower():
                            degree_match = True
                            degree_match_data = {
                                'type': 'degree',
                                'resume_value': user_edu.degree,
                                'job_value': job_degree,
                                'similarity': 100 
                            }
                            break
                    
                    if level_match and degree_match:
                        education_match = 1
                        education_matches.append(level_match_data)
                        education_matches.append(degree_match_data)
            

            job.education_match = education_match
            job.education_matches = education_matches
            
            experience_match = 0
            experience_details = []
            matched_experiences = []
            
            total_years = 0
            resume_experiences = []
            
            for exp in resume.experiences.all():
                if exp.start_date and exp.end_date:
                    delta = exp.end_date - exp.start_date
                    years = delta.days / 365.25 
                    total_years += years
                    
                    resume_experiences.append({
                        'title': exp.title,
                        'company': exp.company,
                        'description': exp.description,
                        'years': round(years, 1)
                    })
            
            job_experiences = Job_Experience.objects.filter(job=job)
            
            for job_exp in job_experiences:
                best_match_score = 0
                best_match_exp = None
                
                for resume_exp in resume_experiences:
                    title_score = fuzz.partial_ratio(
                        resume_exp['title'].lower(), 
                        job_exp.exp_name.lower()
                    )
                    
                    desc_score = 0
                    if job_exp.exp_description and resume_exp['description']:
                        desc_score = fuzz.partial_ratio(
                            resume_exp['description'].lower(),
                            job_exp.exp_description.lower()
                        )
                    
                    combined_score = (title_score * 0.7) + (desc_score * 0.3)
                    
                    if combined_score > best_match_score and combined_score > 70:  # Threshold of 70%
                        best_match_score = combined_score
                        best_match_exp = resume_exp
                
                years_match = False
                if job_exp.exp_type == 'fixed' and job_exp.exp_years is not None:
                    if total_years >= job_exp.exp_years:
                        years_match = True
                        
                elif job_exp.exp_type == 'range' and job_exp.min_exp_years is not None:
                    if total_years >= job_exp.min_exp_years:
                        if job_exp.max_exp_years is None or total_years <= job_exp.max_exp_years:
                            years_match = True
                
                match_details = {
                    'job_requirement': job_exp.exp_name,
                    'job_description': job_exp.exp_description,
                    'years_required': (
                        f"{job_exp.exp_years} years" if job_exp.exp_type == 'fixed'
                        else f"{job_exp.min_exp_years}-{job_exp.max_exp_years} years"
                    ),
                    'years_match': years_match,
                    'total_years': round(total_years, 1),
                    'best_match': best_match_exp,
                    'match_score': round(best_match_score, 1) if best_match_exp else 0
                }
                
                if best_match_exp and best_match_score > 70:
                    matched_experiences.append(match_details)
                
                experience_details.append(match_details)
                
                if years_match and best_match_score > 70:
                    experience_match = 1
            
            job.experience_match = experience_match
            job.experience_details = experience_details
            job.matched_experiences = matched_experiences

            WEIGHTS = {
                'industry': 1,    
                'employment': 1,    
                'location': 1,     
                'skills': 1,        
                'education': 1,    
                'experience': 1     
            }
            
            job.total_score = (
                (job.industry_match * WEIGHTS['industry']) +
                (job.employment_match * WEIGHTS['employment']) +
                (job.location_match * WEIGHTS['location']) +
                (job.skill_match_count * WEIGHTS['skills']) +
                (job.education_match * WEIGHTS['education']) +
                (job.experience_match * WEIGHTS['experience'])
            )
            
            job.max_score = (
                WEIGHTS['industry'] +
                WEIGHTS['employment'] +
                WEIGHTS['location'] +
                (len(job_skills) * WEIGHTS['skills']) + 
                WEIGHTS['education'] +
                WEIGHTS['experience']
            )
            
            match_percentage = (job.total_score / job.max_score) * 100
            job.best_match = match_percentage >= 70
            job.good_match = 50 <= match_percentage < 70
            job.not_suitable = match_percentage < 30
            
            final_jobs.append(job)

        final_jobs.sort(key=lambda job: job.total_score, reverse=True)

    else:
        final_jobs = []
        job_filter = None

    recommended_jobs_count = len(final_jobs)

    context = {
        'job_filter': job_filter,
        'resume_filtered_count': resume_filtered_count,
        'resume_filter': resume_filter,
        'recommended_jobs': final_jobs,
        'recommended_jobs_count': recommended_jobs_count,
        'is_profile_complete': is_profile_complete if employer else False,
        'has_company_jobs': bool(company_jobs) if company else False
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
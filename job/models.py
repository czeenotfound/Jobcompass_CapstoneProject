from django.db import models
from users.models import User 
from company.models import Company
from address.models import Address
from industry.models import Industry
from cloudinary.models import CloudinaryField

import os
import json
from django.conf import settings
from django.core.exceptions import ValidationError

# Load currency data from JSON
CURRENCY_FILE = os.path.join(settings.BASE_DIR, 'static/JS/Common-Currency.json')

with open(CURRENCY_FILE, 'r', encoding='utf-8') as file:
    currency_data = json.load(file)

# Convert JSON to Django choices format
CURRENCY_CHOICES = [
    (code, f'{data["symbol"]}') 
    for code, data in currency_data.items()
]

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    # Expected Salary Display Option
    SALARY_DISPLAY_CHOICES = (
        ('fixed', 'Fixed Salary'),
        ('range', 'Salary Range'),
        ('hidden', 'Do not display'),
    )
    salary_display_type = models.CharField(
        max_length=10, 
        choices=SALARY_DISPLAY_CHOICES, 
        default='fixed'
        ,null=True
        ,blank=True
    )

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PHP')
    salary_fixed = models.PositiveIntegerField(null=True, blank=True, help_text="Enter fixed salary if selected.")
    salary_min = models.PositiveIntegerField(null=True, blank=True, help_text="Enter minimum salary for range.")
    salary_max = models.PositiveIntegerField(null=True, blank=True, help_text="Enter maximum salary for range.")
    salary_mode = models.CharField(
        max_length=10,
        choices=(
            ('Hourly','Hourly'),
            ('Daily','Daily'),
            ('Weekly','Weekly'),
            ('Monthly','Monthly'),
            ('Yearly','Yearly')
        )
        ,null=True
        ,blank=True
    )

    job_description = models.TextField(null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    use_company_location = models.BooleanField(default=False)

    employment_type_choices = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
        ('Internship/OJT', 'Internship/OJT'),
    )
    employment_job_type = models.CharField(max_length=20, choices=employment_type_choices, blank=True)

    location_job_type_choices = (
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
        ('Hybrid', 'Hybrid')
    )
    location_job_type = models.CharField(max_length=20, choices=location_job_type_choices, blank=True)

    posted_date_time = models.DateTimeField(auto_now_add=True)
    
    # for closing or opening job 
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
            
class RequiredSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50, blank=True)
    # minimum_proficiency = models.IntegerField()

    def __str__(self): 
        return f"{self.skill_name} for {self.job}"
    
class Job_Responsibilities(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    res_name = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"responsibilites for {self.job}"
    
class Job_IdealCandidates(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    ideal_name = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"ideal candidates for {self.job}"
    
class Job_Benefits(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    bene_name = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"benefits for {self.job}"
    from django.db import models

class Job_Experience(models.Model):
    EXPERIENCE_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('range', 'Range'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    exp_type = models.CharField(
        max_length=10, choices=EXPERIENCE_TYPE_CHOICES, default='fixed'
    )
    exp_name = models.CharField(max_length=300, blank=True)
    exp_years = models.IntegerField(null=True, blank=True)  # Fixed experience
    min_exp_years = models.IntegerField(null=True, blank=True)  # Experience range (min)
    max_exp_years = models.IntegerField(null=True, blank=True)  # Experience range (max)
    exp_description = models.TextField(blank=True)

    def __str__(self):
        if self.exp_type == 'fixed':
            return f"{self.exp_name} - {self.exp_years} years"
        else:
            return f"{self.exp_name} - {self.min_exp_years}-{self.max_exp_years} years"





class Job_Education(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor’s Degree'),
        ('master', 'Master’s Degree'),
        ('doctorate', 'Doctorate (Ph.D.)'),
        ('vocational', 'Vocational/Technical'),
        ('other', 'Other'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    education_level = models.CharField(
        max_length=20, choices=EDUCATION_LEVEL_CHOICES, null=True, blank=True
    )
    degree = models.CharField(max_length=100, blank=True)

    
    def __str__(self):
        return f"{self.get_education_level_display()} - {self.degree}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Application for {self.job.title} by {self.user.username}"
    
    def start_conversation(self):
        return Conversation.objects.create(application=self)

    def send_message(self, sender, content):
        conversation, created = Conversation.objects.get_or_create(application=self)
        return Message.objects.create(conversation=conversation, sender=sender, content=content)

class ApplicationStatus(models.Model):
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('INTERVIEW', 'Interview Scheduled'),
        ('OFFERED', 'Offered'),
        ('REJECTED', 'Rejected'),
        ('ACCEPTED', 'Accepted'),
    ]
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    status_date = models.DateTimeField(auto_now=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.application} - {self.status}"    
    
class Conversation(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation for {self.application}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} in {self.conversation}"
   

    
class Interview(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ('VIRTUAL', 'Virtual'),
        ('ONSITE', 'Onsite'),
        ('PHONE', 'Phone'),
        ('GROUP', 'Group'),
        ('PANEL', 'Panel'),
        ('OTHER', 'Other'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_type = models.CharField(
        max_length=50,
        choices=INTERVIEW_TYPE_CHOICES,
        default='VIRTUAL',
        null=True,
        blank=True
    )
    interviewer = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.application} on {self.interview_date}"

class Notification(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.application} sent on {self.sent_date}"

class Offer(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PHP')
    salary_fixed = models.PositiveIntegerField(null=True, blank=True, help_text="Enter a fixed salary.")
    salary_min = models.PositiveIntegerField(null=True, blank=True, help_text="Enter minimum salary for range.")
    salary_max = models.PositiveIntegerField(null=True, blank=True, help_text="Enter maximum salary for range.")
    salary_mode = models.CharField(
        max_length=10,
        choices=(
            ('Hourly', 'Hourly'),
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Monthly', 'Monthly'),
            ('Yearly', 'Yearly')
        ),
        null=True,
        blank=True
    )

    benefits = models.TextField(blank=True, null=True)
    offer_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Offer for {self.application}"


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('APPLICANT', 'Applicant Feedback'),
        ('INTERVIEWER', 'Interviewer Feedback'),
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    content = models.TextField()
    rating = models.IntegerField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback_type} for {self.application}"



class SaveJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    save_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'job')  # Prevent duplicate saves

    def __str__(self):
        return f"Saved Job for {self.job.title} by {self.user.username}"
    
# JOB FAIRS
# Custom validator for avatar

class JobFair(models.Model):
    event_held_choices = (
        ('Onsite', 'Onsite'),
        ('Virtual', 'Virtual'),
        ('Hybrid', 'Hybrid')
    )
 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING, null=True, blank=True)

    # if user picks hybrid fill in both
    # if user picks onsite and what site 
    location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobfair')
    # if user picks virtual and what site 
    url_location = models.URLField(null=True, blank=True)
    
    description = models.TextField(blank=True)
    fair_event_held = models.CharField(max_length=20, choices=event_held_choices, blank=True)
    # Additional Fields
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True) 
    end_time = models.TimeField(null=True, blank=True)  
    
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    
    max_attendees = models.IntegerField(null=True, blank=True)

    application_starts =models.DateField(null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    
    image = CloudinaryField(
        'images', 
        folder='job-fair',
        default = "https://res.cloudinary.com/di2hrzuyq/image/upload/v1733062519/luabhrtwak2aeu98sq71.jpg"
    )
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    posted_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Check if avatar is being updated
        if not self.image:  # If there's no image, default image will be used
            self.image = "https://res.cloudinary.com/di2hrzuyq/image/upload/v1733062519/luabhrtwak2aeu98sq71.jpg"
        
        super().save(*args, **kwargs)
    
class JobFairRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobfair = models.ForeignKey(JobFair, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'jobfair')  # Ensure each user can register only once per job fair

    def __str__(self):
        return f"Registration for {self.jobfair.title} by {self.user.username}"
    
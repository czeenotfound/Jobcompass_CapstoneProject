from django.db import models
from users.models import User
from address.models import Address
from industry.models import Industry
from django.core.exceptions import ValidationError
from io import BytesIO
from django.core.files import File
from PIL import Image 
import os
import json
from uuid import uuid4
from cloudinary.models import CloudinaryField

from django.conf import settings

# Load currency data from JSON
CURRENCY_FILE = os.path.join(settings.BASE_DIR, 'static/JS/Common-Currency.json')

with open(CURRENCY_FILE, 'r', encoding='utf-8') as file:
    currency_data = json.load(file)

# Convert JSON to Django choices format
CURRENCY_CHOICES = [
    (code, f'{data["symbol"]}') 
    for code, data in currency_data.items()
]

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = CloudinaryField(
        'avatar', 
        folder='avatar-resume', 
        default="https://res.cloudinary.com/di2hrzuyq/image/upload/v1733062519/pbnrwanwq7rp17jfr92z.png"
    )

    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    suffix = models.CharField   (max_length=10, blank=True)

    about_me = models.TextField(blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='resumes')

   # Expected Salary Display Option
    SALARY_DISPLAY_CHOICES = (
        ('fixed', 'Fixed Salary'),
        ('range', 'Salary Range'),
        ('hidden', 'Do not display'),
    )
    salary_display_type = models.CharField(
        max_length=10, 
        choices=SALARY_DISPLAY_CHOICES, 
        default='hidden'
        ,null=True
        ,blank=True
    )

    # Salary Fields
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PHP', null=True, blank=True)
    expt_salary_fixed = models.PositiveIntegerField(null=True, blank=True, help_text="Enter fixed salary if selected.")
    expt_salary_min = models.PositiveIntegerField(null=True, blank=True, help_text="Enter minimum salary for range.")
    expt_salary_max = models.PositiveIntegerField(null=True, blank=True, help_text="Enter maximum salary for range.")
    expt_salary_mode = models.CharField(
        max_length=20, 
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

    # preferences
    job_position = models.CharField(max_length=150, blank=True)

    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING, null=True, blank=True)
    location_job_type_choices = (
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
        ('Hybrid', 'Hybrid')
    )
    location_job_type = models.CharField(max_length=20, choices=location_job_type_choices, blank=True)

    employment_type_choices = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
        ('Internship/OJT', 'Internship/OJT'),
    )
    employment_job_type = models.CharField(max_length=20, choices=employment_type_choices, blank=True)
    
    upload_resume = CloudinaryField(
        'file', 
        resource_type='raw', 
        folder='resume',
        blank=True
    )

    def __str__(self):
        return f"Resume - {self.first_name} {self.last_name}"

class Skill(models.Model):
    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Skill for {self.user_profile.first_name} {self.user_profile.last_name} - {self.name} "

class Education(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor’s Degree'),
        ('master', 'Master’s Degree'),
        ('doctorate', 'Doctorate (Ph.D.)'),
        ('vocational', 'Vocational/Technical'),
        ('other', 'Other'),
    ]

    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    education_level = models.CharField(
        max_length=20, choices=EDUCATION_LEVEL_CHOICES, null=True, blank=True
    )
    degree = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    graduation_date = models.DateField(blank=True, null=True) 

    def __str__(self):
        return f"{self.get_education_level_display()} - {self.degree} - {self.institution} -  ({self.graduation_date if self.graduation_date else 'N/A'})"
    
class Experience(models.Model):
    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Experience - {self.title} - {self.company}"
    
class Certification(models.Model):
    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Certification - {self.name}"
    
class Project(models.Model):
    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Project - {self.title}"

class SocialLink(models.Model):
    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Social link - {self.platform}"
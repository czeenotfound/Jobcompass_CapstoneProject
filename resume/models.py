from django.db import models
from users.models import User
from address.models import Address
from industry.models import Industry
from django.core.exceptions import ValidationError
import os
from uuid import uuid4

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")

def validate_file_size(value):
    """
    Validator to ensure file size does not exceed 5MB.
    """
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError(f"File size must not exceed 5MB.")
    
def resume_file_upload_path(instance, filename):
    ext = filename.split('.')[-1]  # Get the file extension
    filename = f"{uuid4()}.{ext}"  # Generate a unique filename
    return os.path.join('resume', filename)

    
class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    suffix = models.CharField(max_length=10, blank=True)

    about_me = models.TextField(blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='resumes')

    # preferences
    job_position = models.CharField(max_length=150, blank=True)
    expt_salary_min = models.PositiveIntegerField(null=True, blank=True)
    expt_salary_max = models.PositiveIntegerField(null=True, blank=True)

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
    
    upload_resume = models.FileField(
        upload_to=resume_file_upload_path,
        null=True,
        blank=True,
        validators=[validate_pdf]
    )
    
    def __str__(self):
        return f"Resume - {self.first_name} {self.last_name}"


class Skill(models.Model):
    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Skill - {self.name}"
    
class Education(models.Model):
    user_profile = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Education - {self.degree} - {self.institution} - {self.graduation_year}"
    
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
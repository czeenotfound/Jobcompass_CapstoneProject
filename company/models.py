from django.db import models
from users.models import User
from address.models import Address
from industry.models import Industry
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image  # For image processing
from io import BytesIO
from django.core.files import File
import os
from uuid import uuid4
from cloudinary.models import CloudinaryField

# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    
    avatar = CloudinaryField(
        'avatar',
        folder='company-avatar',
        default="https://res.cloudinary.com/di2hrzuyq/image/upload/v1733062520/lvehkmmijnwrvxvtm1mb.png"
    )
    
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)

    about_us = models.TextField(null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='industries')
    dateFounded = models.DateField(null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='company')
    employee_count = models.PositiveIntegerField(null=True, blank=True)
    
    tin_number = models.CharField(max_length=15, null=True, blank=True)
    
    bir_file = CloudinaryField(
        'file',
        resource_type='raw',
        folder='company-bir',
        blank=True
    )

    dti_file = CloudinaryField(
        'file',
        resource_type='raw', 
        folder='company-dti',
        blank=True
    )

    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Verified', 'Verified'),
            ('Rejected', 'Rejected')
        ],
        default='Pending',
        blank= True
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def __str__(self):
         return f'{self.company_name}'

class Employer(models.Model):
    employer_status_choices = (
        ('CEO', 'Chief Executive Officer (CEO)'),
        ('HR', 'Human Resources (HR)'),
        ('Manager', 'Manager'),
        ('Recruiter', 'Recruiter'),
        ('Staff', 'Staff'),
    )
     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    suffix = models.CharField(max_length=10, blank=True)

    employer_status = models.CharField(
        max_length=50, 
        choices=employer_status_choices, 
        blank=True
    )

    about_me = models.TextField(null=True, blank=True)
    # Integrate Address model into Company
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='employer')

    # Social Media Links
    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_employer_status_display()}"




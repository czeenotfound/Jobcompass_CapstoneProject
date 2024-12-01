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


def validate_file_extension(value):
    """
    Validator to check the file extension. For example, only DOCX and PDF files.
    """
    valid_extensions = ['docx', 'pdf']
    extension = os.path.splitext(value.name)[1][1:].lower()  # Extract the file extension
    if extension not in valid_extensions:
        raise ValidationError(f"File extension must be one of: {', '.join(valid_extensions)}")

def validate_file_size(value):
    """
    Validator to ensure file size does not exceed 5MB.
    """
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError(f"File size must not exceed 5MB.")
    
# Custom validator for avatar
def validate_avatar(image):
    # Check file size (e.g., max 2MB)
    max_file_size = 2 * 1024 * 1024  # 2MB
    if image.size > max_file_size:
        raise ValidationError("Avatar file size must not exceed 2MB.")
    
    # Check file format
    valid_formats = ['JPEG', 'JPG', 'PNG', 'WEBP']
    try:
        img = Image.open(image)
        if img.format.upper() not in valid_formats:
            raise ValidationError(f"Unsupported file format. Use one of the following: {', '.join(valid_formats)}.")
        
        # Check dimensions (e.g., minimum 128x128 pixels)
        min_width, min_height = 128, 128
        if img.width < min_width or img.height < min_height:
            raise ValidationError(f"Avatar dimensions must be at least {min_width}x{min_height} pixels.")
    except Exception as e:
        raise ValidationError("Invalid image file.") from e

# Resize image function
def resize_image(image, max_size=(1280, 1280)):
    """
    """
    img = Image.open(image)
    img = img.convert('RGB')  # Ensure compatibility for saving as JPEG
    
    # Check if the image exceeds the maximum dimensions
    img.thumbnail(max_size, Image.Resampling.LANCZOS)  # Maintain aspect ratio and fit within max_size
    
    # Save the resized image into a buffer
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)  # Adjust quality to reduce file size further if needed
    buffer.seek(0)
    return File(buffer, name=image.name)

def company_file_upload_path(instance, filename):
    ext = filename.split('.')[-1]  # Get the file extension
    filename = f"{uuid4()}.{ext}"  # Generate a unique filename
    return os.path.join('company-file', filename)

def company_avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]  # Get the file extension
    filename = f"{uuid4()}.{ext}"  # Generate a unique filename
    return os.path.join('company', filename)

# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
        
    company_name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(
        upload_to=company_avatar_upload_path,
        null=True, 
        default="office-building.png",
        validators=[validate_avatar]  
    )
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)

    about_us = models.TextField(null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='industries')
    dateFounded = models.DateTimeField(null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='company')
    employee_count = models.PositiveIntegerField(null=True, blank=True)
    
    tin_number = models.CharField(max_length=15, null=True, blank=True)
    bir_file = models.FileField(
        upload_to=company_file_upload_path,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx']),
            validate_file_size
        ]
    )

    dti_file = models.FileField(
        upload_to=company_file_upload_path,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx']),
            validate_file_size 
        ]
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




from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from PIL import Image  # For image processing
from io import BytesIO
from django.core.files import File
import os
from uuid import uuid4

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

def user_avatar_upload_path(instance, filename):
    """
    Define the upload path for user avatars.
    Store files in 'avatar/' with unique filenames to avoid duplicates.
    """
    ext = filename.split('.')[-1]  # Get the file extension
    filename = f"{uuid4()}.{ext}"  # Generate a unique filename
    return os.path.join('avatar', filename)

# Updated User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,  # Use the callable
        null=True, 
        default="icons8-male-user-96.png",
        validators=[validate_avatar]  # Add the custom validator
    )
    phone = models.CharField(max_length=15, null=True, blank=True)

    is_employer = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)

    has_resume = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Resize the avatar if one is provided
        if self.avatar:
            self.avatar = resize_image(self.avatar)
        super().save(*args, **kwargs)
    
    
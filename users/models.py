from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from PIL import Image  # For image processing
from io import BytesIO
from django.core.files import File
import os
from uuid import uuid4
from cloudinary.models import CloudinaryField

# Updated User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = CloudinaryField(
        'avatar', 
        folder='avatar', 
        default="https://res.cloudinary.com/di2hrzuyq/image/upload/v1733062519/pbnrwanwq7rp17jfr92z.png"
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_employer = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    has_resume = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Check if avatar is being updated
        if not self.avatar:  # If there's no avatar, default image will be used
            self.avatar = "https://res.cloudinary.com/di2hrzuyq/image/upload/v1733062519/pbnrwanwq7rp17jfr92z.png"
        
        super().save(*args, **kwargs)
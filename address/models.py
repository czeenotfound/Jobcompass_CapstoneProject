from django.db import models
from users.models import User

# Create your models here.
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.street}, {self.barangay}, {self.city}, {self.province}, {self.region}"
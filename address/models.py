from django.db import models
from users.models import User

# Create your models here.
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    country = models.CharField(max_length=100, blank=True)
    countrycity = models.CharField(max_length=100, blank=True)
    countrypostal = models.CharField(max_length=100, blank=True)
    countrystreet = models.CharField(max_length=100, blank=True)

    region = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.street}, {self.barangay}, {self.city}, {self.province}, {self.region}"
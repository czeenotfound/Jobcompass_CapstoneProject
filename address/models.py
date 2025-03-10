from django.db import models
from django.conf import settings
from users.models import User
import os
import json

# Load JSON Data
COUNTRIES_FILE = os.path.join(settings.BASE_DIR, 'static/JS/countries_states_cities.json')

with open(COUNTRIES_FILE, 'r', encoding='utf-8') as file:
    country_data = json.load(file)

# Generate Country Choices
COUNTRY_CHOICES = [(c["iso2"], c["name"]) for c in country_data]

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, blank=True)
    countrypostal = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.get_country_display()}, {self.countrypostal}, {self.region}, {self.city}, {self.street}"

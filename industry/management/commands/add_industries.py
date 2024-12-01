import json
from django.core.management.base import BaseCommand
from industry.models import Industry

class Command(BaseCommand):
    help = 'Add multiple industries to the database from a JSON file'

    def handle(self, *args, **kwargs):
        # Load the JSON file
        with open('industry.json', 'r') as file:
            data = json.load(file)
        
        # Extract 'label' field from the JSON data
        industries = [item['label'] for item in data['content']]

        # Create Industry objects
        industry_objects = [Industry(name=industry) for industry in industries]

        # Bulk insert the data
        Industry.objects.bulk_create(industry_objects)

        self.stdout.write(self.style.SUCCESS(f"Inserted {len(industries)} industries."))

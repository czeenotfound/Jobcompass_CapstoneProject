from django.shortcuts import render
from .models import Industry

# Path to your file (replace with actual path)
file_path = '../industries.txt'

# Read the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Prepare list for bulk_create
industrys = []

# Iterate over the lines in the file
for line in lines:
    # Strip new lines and split the data by comma
    first_name, last_name = line.strip().split(',')
    
    # Create Industry instances (but don't save them yet)
    industrys.append(Industry(first_name=first_name, last_name=last_name))

# Bulk insert the data into the database
Industry.objects.bulk_create(industrys)

print(f"Inserted {len(industrys)} records into the database.")

# Create your views here.

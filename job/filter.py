import django_filters
from django.db.models import Q
from job.models import Job, JobFair
from industry.models import Industry

def get_salary_range_choices():
    return [
        ("below_15k", "Below PHP 15,000"),
        ("15k_20k", "PHP 15,000 - PHP 20,000"),
        ("20k_30k", "PHP 20,000 - PHP 30,000"),
        ("30k_40k", "PHP 30,000 - PHP 40,000"),
        ("40k_50k", "PHP 40,000 - PHP 50,000"),
        ("50k_75k", "PHP 50,000 - PHP 75,000"),
        ("75k_100k", "PHP 75,000 - PHP 100,000"),
        ("100k_150k", "PHP 100,000 - PHP 150,000"),
        ("150k_200k", "PHP 150,000 - PHP 200,000"),
        ("200k_300k", "PHP 200,000 - PHP 300,000"),
        ("300k_above", "Above PHP 300,000"),
    ]

class Jobfilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(method='filter_location')  
    employment_job_type = django_filters.ChoiceFilter(choices=Job.employment_type_choices, label="Job Type",)
    industry = django_filters.ModelChoiceFilter(
        queryset=Industry.objects.all(),  # Fetch all industries
        label="Industry",
        to_field_name='name',  # Filter by the `name` field of the Industry model
    )
    salary_range = django_filters.ChoiceFilter(
        choices=get_salary_range_choices(),
        method='filter_salary_range',
        label="Salary Range",
        empty_label="Select Salary Range",  # Set the placeholder here
    )

    class Meta:
        model = Job
        fields = ['title', 'location', 'employment_job_type', 'industry', 'salary_min', 'salary_max']  

    def filter_location(self, queryset, name, value):
        return queryset.filter(
            Q(location__region__icontains=value) |
            Q(location__province__icontains=value) |
            Q(location__city__icontains=value) |
            Q(location__barangay__icontains=value) |
            Q(location__street__icontains=value)
        )
    

    def filter_salary_range(self, queryset, name, value):
        salary_ranges = {
            "below_15k": (0, 15000),
            "15k_20k": (15000, 20000),
            "20k_30k": (20000, 30000),
            "30k_40k": (30000, 40000),
            "40k_50k": (40000, 50000),
            "50k_75k": (50000, 75000),
            "75k_100k": (75000, 100000),
            "100k_150k": (100000, 150000),
            "150k_200k": (150000, 200000),
            "200k_300k": (200000, 300000),
            "300k_above": (300000, 10**9),  # Use a very high integer for "above PHP 300,000"
        }
        if value in salary_ranges:
            min_salary, max_salary = salary_ranges[value]
            return queryset.filter(
                Q(salary_min__gte=min_salary, salary_min__lte=max_salary) |
                Q(salary_max__gte=min_salary, salary_max__lte=max_salary)
            )
        return queryset
    

class JobFairfilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(method='filter_location')  
    event_jobfair_type = django_filters.ChoiceFilter(choices=JobFair.event_held_choices, label="Event Type",)
    industry = django_filters.ModelChoiceFilter(
        queryset=Industry.objects.all(),  # Fetch all industries
        label="Industry",
        to_field_name='name',  # Filter by the `name` field of the Industry model
    )

    class Meta:
        model = JobFair
        fields = ['title', 'location', 'start_date', 'industry', 'fair_event_held']  

    def filter_location(self, queryset, name, value):
        return queryset.filter(
            Q(location__region__icontains=value) |
            Q(location__province__icontains=value) |
            Q(location__city__icontains=value) |
            Q(location__barangay__icontains=value) |
            Q(location__street__icontains=value)
        )
    
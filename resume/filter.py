import django_filters
from django.db.models import Q
from resume.models import Resume
from industry.models import Industry

def get_expt_salary_range_choices():
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


class Resumefilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name', label="Name")
    address = django_filters.CharFilter(method='filter_address')  
    employment_job_type = django_filters.ChoiceFilter(
        choices=Resume.employment_type_choices,
        label="Job Type",
    )
    location_job_type = django_filters.ChoiceFilter(
        choices=Resume.location_job_type_choices,
        label="Location Job Type",
    )
    industry = django_filters.ModelChoiceFilter(
        queryset=Industry.objects.all(),  # Fetch all industries
        label="Industry",
        to_field_name='name',  # Filter by the `name` field of the Industry model
    )
    expt_salary_range = django_filters.ChoiceFilter(
        choices=get_expt_salary_range_choices(),
        method='filter_expt_salary_range',
        label="Salary Range",
        empty_label="Select Salary Range",  # Set the placeholder here
    )

    class Meta:
        model = Resume
        fields = [
            'first_name', 'middle_name', 'last_name', 
            'job_position', 'address', 
            'employment_job_type', 'industry', 
            'expt_salary_min', 'expt_salary_max'
        ]

    def filter_name(self, queryset, name, value):
        """Filter resumes by matching the first name, last name, or both."""
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(middle_name__icontains=value) |
            Q(last_name__icontains=value)
        )
    
    def filter_address(self, queryset, name, value):
        return queryset.filter(
            Q(address__region__icontains=value) |
            Q(address__province__icontains=value) |
            Q(address__city__icontains=value) |
            Q(address__barangay__icontains=value) |
            Q(address__street__icontains=value)
        )
    
    def filter_expt_salary_range(self, queryset, name, value):
        expt_salary_ranges = {
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
        if value in expt_salary_ranges:
            min_salary, max_salary = expt_salary_ranges[value]
            return queryset.filter(
                expt_salary_min__gte=min_salary, expt_salary_max__lte=max_salary
            )
        return queryset

    @property
    def count(self):
        """
        Returns the count of filtered results.
        """
        return self.qs.count()
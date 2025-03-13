import django_filters
from django.db.models import Q
from job.models import Job, JobFair, Job_Education
from industry.models import Industry
import django_filters

class Jobfilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(method='filter_location')
    industry = django_filters.ModelChoiceFilter(
        queryset=Industry.objects.all(),  # Fetch all industries
        label="Industry",
        to_field_name='name',  # Filter by the `name` field of the Industry model
    )
    employment_job_type = django_filters.ChoiceFilter(
        choices=Job.employment_type_choices,
        label="Job Type",
        empty_label="Select Job Type"
    )
    education_level = django_filters.ChoiceFilter(
        choices=Job_Education.EDUCATION_LEVEL_CHOICES,
        method='filter_education',
        label="Education Level",
        empty_label="Select Education Level"
    )
    experience = django_filters.NumberFilter(
        method='filter_experience',
        label="Years of Experience"
    )
    salary_display_type = django_filters.ChoiceFilter(
        choices=Job.SALARY_DISPLAY_CHOICES,
        label="Salary Type",
        empty_label="Select Salary Type"
    )

    min_salary = django_filters.NumberFilter(
        method='filter_min_salary',
        label="Minimum Salary"
    )

    max_salary = django_filters.NumberFilter(
        method='filter_max_salary',
        label="Maximum Salary"
    )

    class Meta:
        model = Job
        fields = ['title', 'location', 'employment_job_type', 'education_level', 
                 'experience', 'salary_display_type', 'min_salary', 'max_salary']

    def filter_location(self, queryset, name, value):
        return queryset.filter(
            Q(location__country__icontains=value) |
            Q(location__region__icontains=value) |
            Q(location__city__icontains=value) |
            Q(location__street__icontains=value)
        )
    
    def filter_education(self, queryset, name, value):
        return queryset.filter(job_education__education_level=value).distinct()
    
    def filter_experience(self, queryset, name, value):
        return queryset.filter(
            Q(job_experience__exp_type='fixed', job_experience__exp_years__lte=value) |
            Q(job_experience__exp_type='range', job_experience__min_exp_years__lte=value)
        ).distinct()

    def filter_min_salary(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(salary_display_type='fixed', salary_fixed__gte=value) |
            Q(salary_display_type='range', salary_min__gte=value)
        )

    def filter_max_salary(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(salary_display_type='fixed', salary_fixed__lte=value) |
            Q(salary_display_type='range', salary_max__lte=value)
        )
    
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
            Q(location__city__icontains=value) |
            Q(location__street__icontains=value)
        )
    
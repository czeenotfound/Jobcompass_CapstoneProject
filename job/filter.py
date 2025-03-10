import django_filters
from django.db.models import Q
from job.models import Job, JobFair
from industry.models import Industry

class Jobfilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(method='filter_location')  
    employment_job_type = django_filters.ChoiceFilter(choices=Job.employment_type_choices, label="Job Type",)
    industry = django_filters.ModelChoiceFilter(
        queryset=Industry.objects.all(),  # Fetch all industries
        label="Industry",
        to_field_name='name',  # Filter by the `name` field of the Industry model
    )

    class Meta:
        model = Job
        fields = ['title', 'location', 'employment_job_type', 'industry']  

    def filter_location(self, queryset, name, value):
        return queryset.filter(
            Q(location__country__icontains=value) |
            Q(location__region__icontains=value) |
            Q(location__city__icontains=value) |
            Q(location__street__icontains=value)
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
    
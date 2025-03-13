import django_filters
from django.db.models import Q
from resume.models import Resume
from industry.models import Industry

class Resumefilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name', label="Name")
    address = django_filters.CharFilter(method='filter_address')
    employment_job_type = django_filters.ChoiceFilter(
        choices=Resume.employment_type_choices,
        label="Job Type",
        empty_label="Select Job Type"
    )
    location_job_type = django_filters.ChoiceFilter(
        choices=Resume.location_job_type_choices,
        label="Location Job Type",
    )
    industry = django_filters.ModelChoiceFilter(
        queryset=Industry.objects.all(),
        label="Industry",
        to_field_name='name',
    )
    
    # Updated salary filters to match job filter structure
    salary_display_type = django_filters.ChoiceFilter(
        choices=Resume.SALARY_DISPLAY_CHOICES,
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
        model = Resume
        fields = [
            'name', 'address', 'employment_job_type', 
            'location_job_type', 'industry',
            'salary_display_type', 'min_salary', 'max_salary'
        ]

    def filter_name(self, queryset, name, value):
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

    def filter_min_salary(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(salary_display_type='fixed', expt_salary_fixed__gte=value) |
            Q(salary_display_type='range', expt_salary_min__gte=value)
        )

    def filter_max_salary(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(salary_display_type='fixed', expt_salary_fixed__lte=value) |
            Q(salary_display_type='range', expt_salary_max__lte=value)
        )
    
    @property
    def count(self):
        return self.qs.count()
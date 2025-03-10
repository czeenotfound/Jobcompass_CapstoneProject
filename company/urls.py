from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.register_company, name='register-company'),
    
    path("update-employer-profile/", views.update_employer_profile, name='update-employer-profile'),

    path('manage-jobs/', views.manage_jobs, name='manage-jobs'),
    path('manage-job-fairs/', views.manage_job_fair, name='manage-job-fairs'),

    path('jobfair-registers/<int:pk>', views.jobfair_registers, name='jobfair-registers'),

    path('job-analytics/', views.job_analytics, name='job-analytics'),
    
    path('job-applicants/<int:pk>', views.job_applicants, name='job-applicants'),
    
    path('start-conversation/<int:application_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:pk>/', views.view_conversation, name='view_conversation'),

    path('conversation/<int:pk>/send-message/', views.send_message, name='send_message'),
]   

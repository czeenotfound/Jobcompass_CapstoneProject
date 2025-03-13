from django.urls import path
from . import views

urlpatterns = [
    path('create-job/', views.create_job, name='create-job'),
    path('delete-job/<int:pk>/', views.delete_job, name='delete-job'),
    path('update-job/<int:pk>/', views.update_job, name='update-job'),
    path('activate-job/<int:pk>/', views.activate_job, name='activate-job'),
    path('deactivate-job/<int:pk>/', views.deactivate_job, name='deactivate-job'),


    path('apply-job/<int:pk>/', views.apply, name='apply-job'),
    path('job/<int:pk>/unapply/', views.unapply, name='unapply-job'),

    path('save-job/<int:pk>/', views.save_job, name='save-job'),
    path('job/<int:pk>/unsave/', views.unsave_job, name='unsave-job'),

    path('job-info/<int:pk>/', views.job_info, name='job-info'),
    path('job-fair-info/<int:pk>/', views.job_fair_info, name='job-fair-info'),

    path('job-application/', views.job_application, name='job-application'),
    path('jobfair-registration/', views.jobfair_registration, name='jobfair-registration'),
    path('job-savedjobs/', views.job_savedjobs, name='job-savedjobs'),
    path('application-analytics/', views.application_analytics, name='application-analytics'),


    path('application/<int:pk>/', views.view_job_application, name='view_job_application'),
     
    path('job-fair/', views.job_fair, name="job-fair"),
    path('job-fair/<int:pk>/register/', views.job_fair_register, name='jobfair_register'),
    path('job-fair/<int:pk>/success/', views.jobfair_success, name='jobfair_success'),

    path('all-job-fair/', views.all_job_fair, name="all-job-fair"),

    path('create-job-fair/', views.create_job_fair, name='create-job-fair'),
    path('delete-job-fair/<int:pk>/', views.delete_job_fair, name='delete-job-fair'),
    path('update-job-fair/<int:pk>/', views.update_job_fair, name='update-job-fair'),
    path('activate-job-fair/<int:pk>/', views.activate_job_fair, name='activate-job-fair'),
    path('deactivate-job-fair/<int:pk>/', views.deactivate_job_fair, name='deactivate-job-fair'),

]
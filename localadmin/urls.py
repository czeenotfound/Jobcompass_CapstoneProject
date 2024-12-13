from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="admin-dashboard"),

    path('admin-dashboard/', views.admin_dashboard, name="admin-dashboard"),
    path('admin-profile/<int:pk>/', views.admin_profile, name="admin-profile"),
    

    path('admin-manage-jobs/', views.admin_manage_jobs, name="admin-manage-jobs"),
    path('activate-job/<int:pk>/', views.admin_activate_job, name='admin-activate-job'),
    path('deactivate-job/<int:pk>/', views.admin_deactivate_job, name='admin-deactivate-job'),


    path('admin/toggle-featured-status/<int:pk>/', views.toggle_featured_status, name='toggle-featured-status'),

    path('admin-manage-jobfairs/', views.admin_manage_jobfairs, name="admin-manage-jobfairs"),
    path('activate-job-fair/<int:pk>/', views.admin_activate_job_fair, name='admin-activate-job-fair'),
    path('deactivate-job-fair/<int:pk>/', views.admin_deactivate_job_fair, name='admin-deactivate-job-fair'),


    path('admin-employers/', views.admin_employers, name="admin-employers"),
    path('admin-applicants/', views.admin_applicants, name="admin-applicants"),

    path('admin-verification/', views.admin_verification, name="admin-verification"),

    path('login/', views.login_admin, name="admin-login"),
    path('logout/', views.logout_admin, name="admin-logout"),

    path('toggle-user-status/<int:user_id>/', views.toggle_user_status, name='toggle-user-status'),
]
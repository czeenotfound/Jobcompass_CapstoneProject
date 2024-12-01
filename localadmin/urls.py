from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="admin-dashboard"),

    path('admin-dashboard/', views.admin_dashboard, name="admin-dashboard"),
    path('admin-profile/', views.admin_profile, name="admin-profile"),

    path('admin-settings/', views.admin_settings, name="admin-settings"),
    path('admin-acc-settings/', views.admin_acc_settings, name="admin-acc-settings"),

    path('admin-manage-jobs/', views.admin_manage_jobs, name="admin-manage-jobs"),
    path('admin-manage-jobfairs/', views.admin_manage_jobfairs, name="admin-manage-jobfairs"),
    
    path('admin-employers/', views.admin_employers, name="admin-employers"),
    path('admin-applicants/', views.admin_applicants, name="admin-applicants"),

    path('admin-reports/', views.admin_reports, name="admin-reports"),
    path('admin-verification/', views.admin_verification, name="admin-verification"),

    path('login/', views.login_admin, name="admin-login"),
    path('logout/', views.logout_admin, name="admin-logout"),
]
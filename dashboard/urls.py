from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    
    path('profile/<int:pk>', views.applicant_profile, name="applicant-profile"),
    path('company-profile/<int:pk>', views.company_profile, name="company-profile"),
    path('employer-profile/<int:pk>', views.employer_profile, name="employer-profile"),

    path('resume/<int:pk>/', views.view_resume_profile, name='view-resume-profile'),

    path('settings/<int:pk>/', views.user_settings, name='settings'),

    path('inbox/', views.inbox, name="inbox"),
]
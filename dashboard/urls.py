from django.urls import path
from . import views

urlpatterns = [
    # path('', views.proxy, name ="proxy"),
    # path('applicant-dashboard/', views.applicant_dashboard, name ="applicant-dashboard"),
    # path('employer-dashboard/', views.employer_dashboard, name ="employer-dashboard"),
    path('', views.dashboard, name="dashboard"),

    path('profile/<int:pk>', views.applicant_profile, name="applicant-profile"),
    path('company-profile/<int:pk>', views.company_profile, name="company-profile"),
    path('employer-profile/<int:pk>', views.employer_profile, name="employer-profile"),

    path('resume/<int:pk>/', views.view_resume_profile, name='view-resume-profile'),


    path('inbox/', views.inbox, name="inbox"),
]
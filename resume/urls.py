from django.urls import path
from . import views

urlpatterns = [
    path('create-resume/', views.create_resume, name='create-resume'),
    path('resume-info/<int:pk>', views.resume_info, name='resume-info'),
]

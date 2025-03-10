from django.urls import path
from . import views

app_name = 'skill'

urlpatterns = [
    path('search/', views.search_skills, name='search_skills'),
]
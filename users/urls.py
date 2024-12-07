from django.urls import path
from . import views

urlpatterns = [
    # user autherntication
    # sign in
    path('', views.home, name="home"),
    path('jobfair/', views.job_fair, name="jobfair"),
    
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    # sign up
    path('register/', views.register, name="register"),
]
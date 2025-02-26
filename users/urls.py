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
    path('verify-email/<uidb64>/<token>/', views.verify_email, name="verify_email"),
    path('resend-verification-link/', views.resend_verification_link, name="resend_verification_link"),
    path('password-reset/', views.password_reset_request, name="password_reset_request"),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name="reset_password"),
]
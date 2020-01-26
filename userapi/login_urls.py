from django.urls import path, include, re_path 
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from userapi import login_views 
    
urlpatterns = [

    path('signup/', login_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'),name='login'),
    path('activate_account/<str:token>',login_views.activate_account, name='activate_account'),
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='login/password_reset.html',
            email_template_name='login/password_reset_email.html',
            subject_template_name='login/password_reset_subject.txt'),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='login/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='login/password_reset_confirm.html'),
        name='password_reset_confirm'), 
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='login/password_reset_complete.html'),
        name='password_reset_complete'),
]
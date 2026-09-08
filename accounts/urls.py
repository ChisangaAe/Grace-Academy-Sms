from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Dashboard & User Approvals
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pending-allocation/', views.pending_allocation_view, name='pending_allocation'),
    path('approve/<int:pk>/', views.approve_user, name='approve_user'),
    path('reject/<int:pk>/', views.reject_user, name='reject_user'),

    # Authentication & Registration
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('register/', views.register_teacher, name='register_teacher'),

    # Password Reset Flow
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
         name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
         name='password_reset_complete'),
]
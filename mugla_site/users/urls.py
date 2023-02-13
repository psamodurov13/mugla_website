from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/<str:slug>', ProfileView.as_view(), name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile-avatar/', profile_crop_avatar, name='profile_crop_avatar'),
    path('password-reset/', ResetPassword.as_view(), name='password_reset'),
    path('password-reset/done/', DoneResetPassword.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ConfirmResetPassword.as_view(), name='password_reset_confirm'),
    path('reset/done/', CompleteResetPassword.as_view(), name='password_reset_complete'),
    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', ChangePasswordDone.as_view(), name='password_change_done'),
]
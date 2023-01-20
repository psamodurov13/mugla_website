from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/<str:slug>', ProfileView.as_view(), name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]
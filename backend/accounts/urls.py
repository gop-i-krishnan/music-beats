# This code defines the URL patterns for the accounts app in a Django project.
# It includes paths for user registration, login, profile retrieval, and logout.
# The views for these paths are imported from the views module of the same app.
# The urlpatterns list is used to route incoming requests to the appropriate view based on the URL.
# accounts/urls.py
from django.urls import path
from .views import UserRegistrationView, LoginAPIView, UserProfileView, LogoutAPIView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
]

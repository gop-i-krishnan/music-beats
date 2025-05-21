# accounts/urls.py
    # This code defines the URL patterns for the accounts app in a Django project.
from django.urls import path
from .views import (
    UserRegistrationView, LoginAPIView, UserProfileView, LogoutAPIView,
    AdminOnlyView, TeacherOnlyView, StudentOnlyView, ParentOnlyView, 
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    #role-based views
    path('admin/', AdminOnlyView.as_view(), name='admin-view'),
    path('teacher/', TeacherOnlyView.as_view(), name='teacher-view'),
    path('student/', StudentOnlyView.as_view(), name='student-view'),
    path('parent/', ParentOnlyView.as_view(), name='parent-view'),
]

from django.urls import path
from .views import UserRegistrationView, LoginAPIView ,UserProfileView , LogoutView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]

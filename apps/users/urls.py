from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import WelcomeAPIView, RegistrationAPIView, UserLoginAPIView, UserProfileAPIView, EditProfileView, CreateProfileView

urlpatterns = [
    path('view/', WelcomeAPIView.as_view(), name='user-view'),
    path('register/', RegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),  # New endpoint for editing profile
    path('create-profile/', CreateProfileView.as_view(), name='create-profile'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]


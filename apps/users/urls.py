from django.urls import path
from .views import WelcomeAPIView, RegistrationAPIView, UserLoginAPIView, UserProfileAPIView

urlpatterns = [
    path('view/', WelcomeAPIView.as_view(), name='user-view'),
    path('register/', RegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]

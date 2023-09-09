from django.urls import path
from .views import RegistrationAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user-register'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]

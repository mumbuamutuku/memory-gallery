from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import WelcomeAPIView, RegistrationAPIView, UserLoginAPIView, UserProfileAPIView, CreateProfileAPIView

urlpatterns = [
    path('view/', WelcomeAPIView.as_view(), name='user-view'),
    path('register/', RegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    #path('profile/<int:user_id>/', UserProfileAPIView.as_view(), name='user-profile'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('create-profile/', CreateProfileAPIView.as_view(), name='create-profile'),
]

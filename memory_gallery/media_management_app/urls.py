from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, MediaViewSet

# Create a router and register all the viewsets with it.
router = DefaultRouter()
router.register(r'albums', AlbumViewSet)  # Register the AlbumViewSet for the 'albums' endpoint
router.register(r'media', MediaViewSet)    # Register the MediaViewSet for the 'media' endpoint

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

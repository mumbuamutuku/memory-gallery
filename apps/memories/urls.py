from django.urls import path
from .views import AlbumListCreateView, AlbumDetailView, MemoryListCreateView, MemoryDetailView
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('albums/', AlbumListCreateView.as_view(), name='album-list-create'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('albums/<int:album_id>/memories/', views.MemoriesByAlbumView.as_view(), name='memories-by-album'),
    path('memory/', MemoryListCreateView.as_view(), name='memory-list-create'),
    path('memory/<int:pk>/', MemoryDetailView.as_view(), name='memory-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path
from .views import AlbumListCreateView, AlbumDetailView, MemoryListCreateView, MemoryDetailView

urlpatterns = [
    path('albums/', AlbumListCreateView.as_view(), name='album-list-create'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('memories/', MemoryListCreateView.as_view(), name='memory-list-create'),
    path('memories/<int:pk>/', MemoryDetailView.as_view(), name='memory-detail'),
]

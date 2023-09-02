from django.urls import path
from . import views

app_name = 'media_management_app'

urlpatterns = [
    # URL for the list of albums
    path('albums/', views.album_list, name='album_list'),

    # URL for viewing details of a specific album
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),

    # URL for creating a new album
    path('create_album/', views.create_album, name='create_album'),

    # URL for uploading media to a specific album
    path('album/<int:album_id>/upload_media/', views.upload_media, name='upload_media'),
]

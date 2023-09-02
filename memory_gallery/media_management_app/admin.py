from django.contrib import admin
from .models import Album, Media

# Register the Album model with the Django admin site
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """
    Admin class for managing Album objects in the Django admin site.

    Fields to display and filter in the admin list view are specified here.
    """
    list_display = ('title', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

# Register the Media model with the Django admin site
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """
    Admin class for managing Media objects in the Django admin site.

    Fields to display and filter in the admin list view are specified here.
    """
    list_display = ('title', 'album', 'uploader', 'upload_date', 'privacy_setting')
    list_filter = ('album', 'uploader', 'upload_date', 'privacy_setting')
    search_fields = ('title', 'description')

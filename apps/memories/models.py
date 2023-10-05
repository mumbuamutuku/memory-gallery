from django.db import models
from apps.users.models import CustomUser
from django.utils import timezone

class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_photo = models.ImageField(upload_to='album_covers/', null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Memory(models.Model):
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='memories/', null=True, blank=True)
    video = models.FileField(upload_to='memories/', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='memories')

    def __str__(self):
        return f"Memory {self.id}"


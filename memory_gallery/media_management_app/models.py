from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Media(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    file = models.FileField(upload_t0='media_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(
        max_length=20,
        choices=[
            (private, private),
            (public, public),
        ],
        default='public',

    uploader = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

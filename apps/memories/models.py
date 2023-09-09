from django.db import models
from apps.users.models import CustomUser  # Import the custom user model from the users app

class Album(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Memory(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='memories/', null=True, blank=True)
    video = models.FileField(upload_to='memories/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

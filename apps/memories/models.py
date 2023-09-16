from django.db import models
from apps.users.models import CustomUser  # Import the custom user model from the users app

class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  
    cover_photo = models.ForeignKey('Memory', on_delete=models.SET_NULL, null=True, blank=True, related_name='cover_for_albums')
    date_created = models.DateTimeField(auto_now_add=True)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    memories = models.ManyToManyField('Memory', related_name='albums', blank=True)

    def __str__(self):
        return self.title

class Memory(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='memories/', null=True, blank=True)
    video = models.FileField(upload_to='memories/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

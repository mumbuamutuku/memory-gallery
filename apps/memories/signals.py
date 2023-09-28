from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Memory
from django.contrib.auth.models import User
import os
from django.core.email import send_mail

@receiver(post_save, sender=Memory)
def handle_memory_creation(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        message = f'New memory created: {instance.title}'
        
        send_notification(user, message)

def send_notification(user, message):
    subject = 'New Memory Created'
    from_email = os.getenv('EMAIL_HOST_USER')
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

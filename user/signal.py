from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User_Data

@receiver(post_save, sender= User_Data)
def send_notification(sender, instance, **kwargs):
    subject = 'User Create New Post '
    message = f'Hi {instance.author.username},\n\nA new post "{instance.title}" has been created.'
    from_email = 'noreply@example.com'
    recipient_list = [instance.author.email]
    
    send_mail(subject, message, from_email, recipient_list)

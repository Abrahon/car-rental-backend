# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User 

@receiver(post_save, sender=User)
def send_approval_notification(sender, instance, created, **kwargs):
    # Only send email when the dealer is approved (is_approved updated to True)
    if not created and instance.is_approved and 'update_fields' in kwargs and 'is_approved' in kwargs['update_fields']:
        send_mail(
            'Dealer Approved',
            'Your account has been approved by Admin.',
            settings.DEFAULT_FROM_EMAIL,  # recommended
            [instance.email]
        )


